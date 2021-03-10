"""
TODO: find solution for lonely points which get their own voxel
TODO: implement tree structure to print/save
TODO: make general Analyzer class to inherit from (make full code packable)
TODO: keep track of earliest voxel in Octree
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from itertools import combinations, product
from Lightcone_approach.LightningAnalyzer import ListNode
from anytree import RenderTree

MAX_POINTS_PER_VOXEL = 10
LIST_OF_COLORS = ['#153e90', '#54e346', '#581845', '#825959', '#89937f', '#0e49b5', '#4e89ae', '#f1fa3c',
                  '#e28316', '#43658b', '#aa26da', '#fa163f', '#898d90', '#fa26a0', '#05dfd7', '#a3f7bf',
                  '#d68060', '#532e1c', '#59886b', '#db6400']


def plot_cube(ax, center, side_length, color="b"):
    """
    From https://stackoverflow.com/questions/11140163/plotting-a-3d-cube-a-sphere-and-a-vector-in-matplotlib#11156353
    """
    r_x = [center[0] - side_length / 2, center[0] + side_length / 2]
    r_y = [center[1] - side_length / 2, center[1] + side_length / 2]
    r_z = [center[2] - side_length / 2, center[2] + side_length / 2]
    for s, e in combinations(np.array(list(product(r_x, r_y, r_z))), 2):
        if side_length + 0.0001 >= np.sum(np.abs(s - e)) >= side_length - 0.0001:
            ax.plot3D(*zip(s, e), color=color)


class Voxel:
    def __init__(self, center: np.array, edge, parent=None):
        self.center = center
        self.edge = edge
        self.parent = parent
        self.neighbours = []
        self.children = []
        self.contents = np.array([])
        self.active = True
        self.label = None
        self.selected = False

    def set_contents(self, contents=None):
        if contents is not None:
            self.contents = contents
        else:
            print("No contents given to set")

    def set_label(self):
        """
        Set the label of the voxel, not counting the irrelevant neighbours.
        Legend of the labels:
            0 = split should be reverted
            1 = Endpoint
            2 = Branch
            3 = Branching point
        """
        modifier = self.check_neighbours()
        if (len(self.neighbours) - modifier) < 4:
            self.label = len(self.neighbours)

    def set_neighbours(self):
        self.neighbours.extend(self.parent.children)
        self.neighbours.remove(self)

        self._look_for_neighbours(self.parent.neighbours)

    def check_neighbours(self):
        """
        Check whether some neighbours have only self an other neighbours as their neighbours. These should not be
        counted when assigning the label.
        :return: Number of neighbours which are not relevant for the counting.
        """
        fake = 0
        check_list = self.neighbours
        for neighbour in self.neighbours:
            count = 0
            for nn in neighbour.neighbours:
                if nn not in check_list:
                    count += 1
            if count == 0:
                fake += 1
        return fake

    def check_parent_relation(self):
        """
        Check rule set for possible parent-child labels, to see if the split produced sensible results.
        :return: not None if the split should be reverted.
        """
        if self.label == 1:
            if self.parent.label != 1:
                return self

        if self.parent.label == 2:
            if self.label == 2:
                self.active = False

        return None

    def _is_neighbour(self, other):
        return (other.edge + self.edge) / np.sqrt(2) >= np.linalg.norm(other.center - self.center)

    def _look_for_neighbours(self, possible_neighbours):
        for neighbour in possible_neighbours:
            if len(neighbour.children) == 0:
                if self._is_neighbour(neighbour):
                    self.neighbours.append(neighbour)
            else:
                self._look_for_neighbours(neighbour.children)

    def split(self):
        new_length = self.edge / 2
        self.active = False

        self.children = [
            Voxel(self.center + np.array([new_length / 2, new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([new_length / 2, new_length / 2, -new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([new_length / 2, -new_length / 2, -new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([new_length / 2, -new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, -new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, new_length / 2, -new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, -new_length / 2, -new_length / 2]), new_length, parent=self)]

        return self.children

    def remove_child(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            print(f'The voxel{child} is not a child of {self}')

    def force_endpoint(self):
        # Find the child with the least amount of neighbours
        number = [len(child.neighbours) for child in self.children]
        ind = number.index(min(number))

        # Find the closest neighbour to that child
        distance_to_neigh = []
        for neighbour in self.children[ind].neighbours:
            distance_to_neigh.append(np.linalg.norm(neighbour.center - self.center))
        n_ind = distance_to_neigh.index(min(distance_to_neigh))

        # Make the selected child an endpoint with the closest neighbour as its only neighbour
        self.children[ind].label = 1
        self.children[ind].neighbours = [self.children[ind].neighbours[n_ind]]

        return self.children[ind]


class Octree:
    def __init__(self, t, x, y, z):
        txyz = sorted(zip(t, x, y, z))
        self.t, self.x, self.y, self.z = map(np.array, zip(*list(txyz)))

        center = np.array([(x.min() + x.max()) / 2, (y.min() + y.max()) / 2, (z.min() + z.max()) / 2])
        longest_side = np.max([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()])

        self.root = Voxel(center, longest_side + 1)
        self.root.set_contents(np.array(range(len(self.t))))

        self.active_leaves = []
        self.endpoints = []
        self.earliest_voxel = self.root

    def set_voxel_contents(self, voxel: Voxel):
        if voxel.parent is not None:
            xmin = self.x[voxel.parent.contents] >= (voxel.center[0] - voxel.edge / 2)
            xmax = self.x[voxel.parent.contents] < (voxel.center[0] + voxel.edge / 2)

            ymin = self.y[voxel.parent.contents] >= (voxel.center[1] - voxel.edge / 2)
            ymax = self.y[voxel.parent.contents] < (voxel.center[1] + voxel.edge / 2)

            zmin = self.z[voxel.parent.contents] >= (voxel.center[2] - voxel.edge / 2)
            zmax = self.z[voxel.parent.contents] < (voxel.center[2] + voxel.edge / 2)

            voxel.set_contents(voxel.parent.contents[xmin * xmax * ymin * ymax * zmin * zmax])

            # Keep track of the voxel containing the earliest point in time
            if voxel.parent == self.earliest_voxel:
                if 0 in voxel.contents:
                    self.earliest_voxel = voxel
        else:
            voxel.set_contents()

    def set_contents(self):
        for voxel in self.active_leaves:
            self.set_voxel_contents(voxel)

    def count_neighbours(self):
        count = []
        for voxel in self.active_leaves:
            count.append(len(voxel.neighbours))
        print(count)

    def remove_empty_voxels(self):
        active_leaves = []
        for leaf in self.active_leaves:
            if len(leaf.contents) == 0:
                leaf.parent.remove_child(leaf)
                leaf.active = False
            else:
                active_leaves.append(leaf)
        self.active_leaves = active_leaves

    def revert_split(self, parent: Voxel):
        parent.active = False
        for child in parent.children:
            child.parent = None
            self.active_leaves.remove(child)
        parent.children = []

    def split_active(self):
        new_leaves = []
        for ind in range(len(self.active_leaves)):
            if self.active_leaves[ind].active:
                children = self.active_leaves[ind].split()
                new_leaves.extend(children)
        self.active_leaves = new_leaves

    def first_split(self):
        children = self.root.split()
        self.active_leaves.extend(children)
        for child in children:
            self.set_voxel_contents(child)
            child.label = 1

        self.remove_empty_voxels()
        self.endpoints = self.active_leaves
        for leaf in self.active_leaves:
            leaf.set_neighbours()

    def refine(self):
        self.first_split()

        while len(self.active_leaves) > 0:
            new_endpoints = []
            # Print the number of neighbours of current active leaves
            self.count_neighbours()

            # Split every active voxel into 8 parts
            self.split_active()

            # Set the contents of newly formed voxels
            self.set_contents()

            # Remove the empty voxels from the list
            self.remove_empty_voxels()

            # Set the neighbours for every voxel which is not empty and label them accordingly
            revert_parents = set()
            for leaf in self.active_leaves:
                leaf.set_neighbours()
                leaf.set_label()
                if leaf.label == 0:
                    revert_parents.add(leaf.parent)
                elif leaf.label == 1:
                    new_endpoints.append(leaf)

            # Check if the voxels are still active: check neighbours and revert split if voxel is disconnected
            for parent in revert_parents:
                self.revert_split(parent)

            # Check if every previous endpoints still have an endpoint child
            for end in self.endpoints:
                labels = [child.label for child in end.children]
                if len(labels) > 0 and 1 not in labels:
                    new_endpoints.append(end.force_endpoint())

            # Check if the voxels are still active: check relation with parent
            revert_parents.clear()
            for voxel in self.active_leaves:
                result = voxel.check_parent_relation()
                if result is not None:
                    new_endpoints.remove(result)
                    revert_parents.add(result.parent)

            # Revert split if voxel is in an impossible situation
            for parent in revert_parents:
                self.revert_split(parent)

            # Update list of endpoints
            self.endpoints = new_endpoints

    def find_leaves(self, voxel: Voxel):
        """
        Find all the leaves in the Octree starting at a given voxel as the root.
        """
        leaves = []
        for child in voxel.children:
            if len(child.children) == 0:
                leaves.append(child)
            else:
                leaves.extend(self.find_leaves(child))

        return leaves

    def plot(self):
        leaves = self.find_leaves(self.root)

        fig = plt.figure(1, figsize=(20, 10))
        ax1 = fig.add_subplot(111, projection='3d')

        cmap = cm.plasma
        norm = mcolors.Normalize(vmin=self.t.min(), vmax=self.t.max())

        ax1.scatter(self.x, self.y, self.z, marker='x', c=self.t, cmap=cmap, norm=norm)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('Voxels tracing the lightning signal')
        for leaf in leaves:
            # print(f"Leaf has its center at {leaf.center} with edge length {leaf.edge}")
            if leaf == self.earliest_voxel:
                print(f"Earliest leaf has its center at {leaf.center} with edge length {leaf.edge}")
                plot_cube(ax1, leaf.center, leaf.edge, color="r")
            else:
                plot_cube(ax1, leaf.center, leaf.edge)

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()


class Analyzer:
    def __init__(self, t, x, y, z, max_branch=100):
        self.octree = Octree(t, x, y, z)
        self.tree = ListNode('root')
        self.lonely = ListNode('lonely')
        self.labelling = True
        self.counter = 0
        self.max_branch = max_branch

    def find_earliest_voxel(self):
        leaves = self.octree.find_leaves(self.octree.root)
        for leaf in leaves:
            if 0 in leaf.contents:
                return leaf

    def find_next_voxel(self, voxel: Voxel):
        start_time = voxel.contents[-1]

        next_counter = 0
        nextBP = voxel.neighbours[next_counter]
        while nextBP.selected or (nextBP.contents[0] < start_time):
            next_counter += 1
            nextBP = voxel.neighbours[next_counter]
            if next_counter == 2:
                return None

        return nextBP

    def find_branch(self, start: Voxel):
        pool = []
        nextBP = start

        while len(nextBP.neighbours) < 3:
            pool.extend(nextBP.contents)
            nextBP = self.find_next_voxel(nextBP)
            nextBP.selected = True
            if nextBP is None:
                break

        return pool, nextBP

    def insert_branch(self, start: Voxel, branch: ListNode):
        if self.counter >= self.max_branch:
            return

        pool1, nextBP1 = self.find_branch(start)
        new_node1 = ListNode('n' + str(self.counter), pool1, parent=branch)
        self.counter += 1

        pool2, nextBP2 = self.find_branch(start)
        new_node2 = ListNode('n' + str(self.counter), pool2, parent=branch)
        self.counter += 1

        if nextBP1 is not None:
            self.insert_branch(nextBP1, new_node1)
        if nextBP2 is not None:
            self.insert_branch(nextBP2, new_node2)

    def label(self):
        self.octree.refine()
        start = self.find_earliest_voxel()
        # if start.label is not 1:
        #     raise Exception("Must start from an endpoint")

        start.selected = True
        pool, BP = self.find_branch(start)
        new_node = ListNode('n' + str(self.counter), pool, parent=self.tree)
        self.counter += 1

        if BP is not None:
            self.insert_branch(BP, new_node)

    def plot_tree(self):
        fig = plt.figure(1, figsize=(20, 10))

        x_plot = self.octree.x
        y_plot = self.octree.y
        z_plot = self.octree.z
        t_plot = self.octree.t

        cmap = cm.plasma
        norm = mcolors.Normalize(vmin=t_plot[0], vmax=t_plot[-1])

        ax1 = fig.add_subplot(121, projection='3d')
        ax1.scatter(x_plot, y_plot, z_plot, marker='^', c=t_plot, cmap=cmap, norm=norm)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('Time ordered original data')

        ax2 = fig.add_subplot(122, projection='3d')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('Branches selected by the algorithm')
        (left, right) = ax1.get_xlim3d()
        ax2.set_xlim3d(left, right)
        (left, right) = ax1.get_ylim3d()
        ax2.set_ylim3d(left, right)
        (left, right) = ax1.get_zlim3d()
        ax2.set_zlim3d(left, right)

        counter = 0
        for _, _, node in RenderTree(self.tree.children[0]):
            color = mcolors.hex2color(LIST_OF_COLORS[int(counter % len(LIST_OF_COLORS))])
            ax2.scatter([x_plot[ind] for ind in node], [y_plot[ind] for ind in node], [z_plot[ind] for ind in node],
                        color=color, marker='o')
            ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')
            counter += 1

        for _, _, node in RenderTree(self.lonely):
            ax2.scatter([x_plot[ind] for ind in node], [y_plot[ind] for ind in node],
                        [z_plot[ind] for ind in node], color='k', marker='s')
            if node.name == 'lonely':
                continue
            ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()
