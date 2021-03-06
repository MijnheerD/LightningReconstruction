"""
TODO: incorporate lonely voxels -> do not use them in mst
"""

from numpy import concatenate, zeros, where, sum, setdiff1d
from scipy.sparse import lil_matrix, diags
from scipy.sparse.csgraph import minimum_spanning_tree
from Analyzer_template import LightningReconstructor, ListNode
from Mesh_approach.Mesh_octree import Octree


def dfc(sym_graph, current_vertex, visited=None):
    # visited is supposed to start at [counter]
    if visited is None:
        visited = []

    # current vertex is index in final_voxels list
    visited.append(current_vertex)
    # we want at least 3 other visited voxels, apart from counter
    if len(visited) > 3:
        return visited

    # assumes graph is in scipy.sparse form and symmetric!
    for neighbour_index in sym_graph[current_vertex].nonzero()[1]:
        if neighbour_index not in visited:
            visited = dfc(sym_graph, neighbour_index, visited)
            if len(visited) > 3:
                return visited

    return visited


class Analyzer(LightningReconstructor):
    def __init__(self, t, x, y, z, min_voxel_size=100, max_voxel_size=10000, max_branch=100):
        super().__init__(max_branch, 'Mesh')

        self.octree = Octree(t, x, y, z)
        self.min_voxel_size = min_voxel_size
        self.max_voxel_size = max_voxel_size
        # To be filled in by label function
        self.voxels = None
        self.removed = None
        self.connections = None
        self.branching_points = None

    def get_x(self):
        return self.octree.x

    def get_y(self):
        return self.octree.y

    def get_z(self):
        return self.octree.z

    def get_t(self):
        return self.octree.t

    def find_begin_voxel(self):
        endpoints = where(sum(self.connections, axis=1) == 1)
        minimum = 1000
        minimum_leaf_ind = None
        for ind in endpoints[0]:
            if ind in self.removed:
                continue
            leaf = self.voxels[ind]
            if min(leaf.contents) < minimum:
                minimum = min(leaf.contents)
                minimum_leaf_ind = ind
                if minimum == 0:
                    break
        return minimum_leaf_ind

    def find_next_branch(self, graph, start, previous=None):
        if previous is None:
            previous = start
        next_voxel = start

        # Collect the indices of the data points inside the branch
        branch = []
        while next_voxel not in self.branching_points:
            branch.extend(self.voxels[next_voxel].contents)
            neighbours = graph[next_voxel].nonzero()[1]
            if sum(self.connections[next_voxel]) > 2:
                # If the voxel has more connections than anticipated, absorb the least important ones
                for nn in neighbours:
                    if sum(self.connections[nn]) == 1:
                        # Sum == 1 implies a voxel which had a trivial connection, but absorbed it
                        self.voxels[next_voxel].contents = concatenate([self.voxels[next_voxel].contents,
                                                                        self.voxels[nn].contents])
                        neighbours = neighbours[neighbours != nn]
                if len(neighbours) > 2:
                    raise Exception("Cannot handle this situation: too many neighbours")
                elif len(neighbours) == 1:
                    # We have removed all neighbours except 1, which should be previous
                    break
            elif sum(self.connections[next_voxel]) == 1:
                if previous != next_voxel:
                    break
            for nn in neighbours:
                if nn != previous and nn not in self.removed:
                    previous = next_voxel
                    next_voxel = nn
                    break
                if nn == neighbours[-1]:
                    raise Exception("No next voxel to find here!")

        # Put all the data points of the branching point in the current branch
        # TO BE UPDATED WITH PROPER DISTRIBUTION FUNCTION
        branch.extend(self.voxels[next_voxel].contents)

        # If we are at a branching point, find the next points to start searching from
        neighbours = graph[next_voxel].nonzero()[1]
        neighbours = neighbours[neighbours != previous]

        # Make sure to not pass on removed voxels
        return_neighbours = setdiff1d(neighbours, self.removed)

        return branch, next_voxel, return_neighbours

    def find_branches(self, sym, start_voxel, branch: ListNode, previous=None):
        if self.counter >= self.max_branch:
            return

        pool, end_voxel, next_points = self.find_next_branch(sym, start_voxel, previous)
        new_node = ListNode('n' + str(self.counter), pool, parent=branch)
        self.counter += 1

        if len(next_points) > 0:
            self.find_branches(sym, next_points[0], new_node, previous=end_voxel)
            self.find_branches(sym, next_points[1], new_node, previous=end_voxel)
        else:
            return

    def make_mst(self):
        # Make the adjacency matrix of the voxel configuration/graph
        connections = lil_matrix((len(self.voxels), len(self.voxels)), dtype='f')  # use float32 to use less memory
        for counter in range(len(self.voxels)):
            nn = self.voxels[counter].neighbours
            for neighbour in nn:
                # Some reverted voxels are not properly removed from neighbour lists and these can lead to ValueErrors
                try:
                    pointer = self.voxels.index(neighbour)
                    ninfo = nn[neighbour]
                    connections[counter, pointer] = ninfo[1].astype('f')
                except ValueError:
                    pass

        # Construct the minimum spanning tree and make it diagonal
        mst = minimum_spanning_tree(connections)
        sym = mst + mst.T - diags(mst.diagonal(), dtype='f')

        return sym

    def count_connections(self, sym):
        connections = zeros((len(self.voxels), 3))
        bp = []
        removed = []
        normal_to_absorb = []
        for counter in range(len(self.voxels)):
            for neighbour in sym[counter].nonzero()[1]:
                number_of_connections = len(dfc(sym, neighbour, visited=[counter])) - 1
                if number_of_connections == 1:
                    # trivial connection / should be absorbed
                    # connections[counter][0] += 1  # Do not count, otherwise find_start_voxel() broken
                    # Absorb the data points of neighbour into the current voxels
                    self.voxels[counter].contents = concatenate([self.voxels[counter].contents,
                                                                 self.voxels[neighbour].contents])
                    removed.append(neighbour)
                    # Next two lines are not advised for csr matrix
                    # sym[counter, neighbour] = 0
                    # sym[neighbour, counter] = 0
                elif number_of_connections == 2:
                    # normal connection / to absorb if too many connections
                    connections[counter][1] += 1
                    normal_to_absorb.append(neighbour)
                else:
                    # heavy connection / important, voxel type defining connection
                    connections[counter][2] += 1

            if connections[counter][2] >= 3:
                bp.append(counter)

            if connections[counter][2] >= 2:
                if connections[counter][1] > 0:
                    for neighbour in normal_to_absorb:
                        self.voxels[counter].contents = concatenate([self.voxels[counter].contents,
                                                                     self.voxels[neighbour].contents])
                        removed.append(neighbour)
                        # sym[counter, neighbour] = 0
                        # sym[neighbour, counter] = 0

            normal_to_absorb = []

        self.connections = connections
        self.branching_points = bp

        return removed

    def label(self):
        lonely = self.octree.refine(min_side=self.min_voxel_size, max_side=self.max_voxel_size)
        self.voxels = self.octree.find_leaves()
        for lone in lonely:
            try:
                pointer = self.voxels.index(lone)
                self.lonely.extend(self.voxels[pointer].contents)
            except ValueError:
                pass

        sym = self.make_mst()
        self.removed = self.count_connections(sym)
        start_voxel = self.find_begin_voxel()

        self.voxels[start_voxel].selected = True
        self.find_branches(sym, start_voxel, self.tree)
