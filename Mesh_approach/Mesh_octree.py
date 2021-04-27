"""
TODO: fake neighbour tool does not work properly, more neighbours may be present
TODO: endpoints are never initialized/not enforced in minimum voxel size
TODO: revisit check_parent_relation and labelling
TODO: scoring method is very slow for large voxels with lots of data points
"""

import numpy as np
from itertools import combinations, product

MAX_POINTS_PER_VOXEL = 10
MIN_DENSITY = 0.01  # Number of points per unit length of edge


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
        self.neighbours = {}
        self.children = []
        self.contents = np.array([])
        self.active = True
        self.label = None
        self.selected = False

    def get_neighbours(self):
        return list(self.neighbours.keys())

    def get_neighbours_types(self):
        return [val[0] for val in self.neighbours.values()]

    def get_neighbours_scores(self):
        return [val[1] for val in self.neighbours.values()]

    def set_score(self, neighbour, score):
        tup = self.neighbours[neighbour]
        self.neighbours[neighbour] = [tup[0], score]

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
            self.label = int(len(self.neighbours) - modifier)

    def set_neighbours(self, final=False):
        if not final:
            for child in self.parent.children:
                if child is not self:
                    self.add_neighbour(child)

            self._look_for_neighbours(self.parent.get_neighbours())
        else:
            final_neighbours = self.get_neighbours()  # Dictionary ensures unique neighbours only
            self.neighbours = {}
            self._look_for_neighbours(final_neighbours)

    def add_neighbour(self, neighbour):
        neighbour_type = self._is_what_neighbour(neighbour)
        if neighbour_type:
            self.neighbours[neighbour] = [neighbour_type, 0]
            return True
        else:
            return False

    def check_neighbours(self):
        """
        Check whether some neighbours have only self an other neighbours as their neighbours. These should not be
        counted when assigning the label.
        :return: Number of neighbours which are not relevant for the counting.
        """
        fake = 0
        check_list = [self]
        check_list.extend(self.get_neighbours())
        n_neighbours = [[] for _ in check_list]
        index = 0
        for neighbour in self.get_neighbours():
            nn = []
            for el in neighbour.neighbours:
                if el not in check_list:
                    nn.append(el)
            n_neighbours[index] = nn
            if len(nn) == 0:
                fake += 1
            else:
                for i in range(index):
                    if set(nn) == set(n_neighbours[i]):
                        fake += 1
            index += 1
        return fake

    def score_all_neighbours(self, x_data, y_data, z_data, neighbours=None):
        if neighbours is None:
            neighbours = self.neighbours
        for neighbour in neighbours:
            score = self._score_neighbour(neighbour, x_data, y_data, z_data)
            self.neighbours[neighbour][1] = score

    def _look_for_neighbours(self, possible_neighbours):
        for neighbour in possible_neighbours:
            if len(neighbour.children) == 0:
                self.add_neighbour(neighbour)
            else:
                self._look_for_neighbours(neighbour.children)

    def _is_neighbour(self, other):
        # np.linalg.norm rounds the result, so we need to allow for some numerical difference
        # Only accounts for edge sharing and face sharing neighbours
        return (other.edge + self.edge) / np.sqrt(2) + 1e-5 >= np.linalg.norm(other.center - self.center)

    def _is_corner_neighbour(self, other):
        return (other.edge + self.edge) * np.sqrt(3) / 2 + 1e-5 >= np.linalg.norm(other.center - self.center)

    def _is_what_neighbour(self, other):
        if self._is_corner_neighbour(other):
            lower_x_bound = other.center[0] >= self.center[0] - self.edge / 2 - 1e-5
            lower_y_bound = other.center[1] >= self.center[1] - self.edge / 2 - 1e-5
            lower_z_bound = other.center[2] >= self.center[2] - self.edge / 2 - 1e-5
            higher_x_bound = other.center[0] <= self.center[0] + self.edge / 2 + 1e-5
            higher_y_bound = other.center[1] <= self.center[1] + self.edge / 2 + 1e-5
            higher_z_bound = other.center[2] <= self.center[2] + self.edge / 2 + 1e-5

            x_bound = lower_x_bound * higher_x_bound
            y_bound = lower_y_bound * higher_y_bound
            z_bound = lower_z_bound * higher_z_bound

            number = np.sum([x_bound, y_bound, z_bound])
            if self._is_corner_neighbour(other):
                if number == 2:
                    return 'face'
                elif number == 1:
                    return 'edge'

            if number == 0:
                return 'corner'

        return False

    def _score_neighbour(self, other, x_data, y_data, z_data):
        # neighbour_type = self.neighbours[other][0]
        self_data = self.contents
        other_data = other.contents

        # Closest distance between two data points is the important factor in connection strength between 2 voxels
        distances = np.zeros((len(self_data), len(other_data)))
        for i in range(len(self_data)):
            for j in range(len(other_data)):
                self_point = np.array([x_data[self_data[i]], y_data[self_data[i]], z_data[self_data[i]]])
                other_point = np.array([x_data[other_data[j]], y_data[other_data[j]], z_data[other_data[j]]])
                distances[i][j] = np.linalg.norm(self_point - other_point)
        # noinspection PyArgumentList
        score = distances.min()

        '''
        # Whether the voxels connect over a face, edge or corner also indicates the connection strength
        if neighbour_type == 'edge':
            score *= 3
        elif neighbour_type == 'corner':
            score *= 5

        # Connection to voxels with a too low density are disfavoured
        if len(other.contents) / other.edge < MIN_DENSITY:
            score *= 2
        '''

        return score

    def check_parent_relation(self):
        """
        Check rule set for possible parent-child labels, to see if the split produced sensible results.
        :return: not None if the split should be reverted.
        """
        if self.label == 1:
            if self.parent.label != 1:
                return self

        if self.parent.label == 2:
            if self.label == 2 and len(self.contents) < MAX_POINTS_PER_VOXEL:
                self.active = False

        return None

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

        # Find the neighbour of that child with the lowest score (= best connection)
        best_neighbour = min(self.children[ind].neighbours, key=lambda k: self.children[ind].neighbours[k][1])

        # Make the selected child an endpoint with the closest neighbour as its only neighbour
        self.children[ind].label = 1
        self.children[ind].neighbours = {best_neighbour: self.children[ind].neighbours[best_neighbour]}

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

    def set_voxel_contents(self, voxel: Voxel):
        if voxel.parent is not None:
            xmin = self.x[voxel.parent.contents] >= (voxel.center[0] - voxel.edge / 2)
            xmax = self.x[voxel.parent.contents] <= (voxel.center[0] + voxel.edge / 2)

            ymin = self.y[voxel.parent.contents] >= (voxel.center[1] - voxel.edge / 2)
            ymax = self.y[voxel.parent.contents] <= (voxel.center[1] + voxel.edge / 2)

            zmin = self.z[voxel.parent.contents] >= (voxel.center[2] - voxel.edge / 2)
            zmax = self.z[voxel.parent.contents] <= (voxel.center[2] + voxel.edge / 2)

            voxel.set_contents(voxel.parent.contents[xmin * xmax * ymin * ymax * zmin * zmax])

        else:
            voxel.set_contents()

    def set_contents(self):
        for voxel in self.active_leaves:
            self.set_voxel_contents(voxel)

    def set_final_neighbours(self):
        final_voxels = self.find_leaves(self.root)
        for leaf in final_voxels:
            # Search through all the neighbours and find final_voxels which are neighbours
            leaf.set_neighbours(final=True)

        for leaf in final_voxels:
            # Check for potentially missed links, as set_neighbours() only looks down
            for neighbour in leaf.get_neighbours():
                if leaf not in neighbour.get_neighbours():
                    neighbour.add_neighbour(leaf)
                    # If neighbour has a lower index in final_voxels, it will not score leaf
                    neighbour.score_all_neighbours(self.x, self.y, self.z, neighbours=[leaf])

            # Score all the neighbours
            leaf.score_all_neighbours(self.x, self.y, self.z)

            # Set the label
            leaf.set_label()

        return final_voxels

    def count_neighbours(self):
        count = []
        for voxel in self.active_leaves:
            count.append(len(voxel.neighbours))
        print(count)

    def remove_empty_voxels(self):
        active_leaves = []
        for leaf in self.active_leaves:
            if len(leaf.contents) == 0:
                # noinspection PyUnresolvedReferences
                leaf.parent.remove_child(leaf)
                # Disconnect the child from the tree completely
                leaf.parent = None
                leaf.neighbours = {}
                leaf.active = False
            else:
                active_leaves.append(leaf)
        self.active_leaves = active_leaves

    def revert_split(self, parent: Voxel):
        parent.active = 2
        for child in parent.children:
            # Tell every neighbour that the child does not exist anymore : update neighbour information
            for neighbour in child.get_neighbours():
                if neighbour not in parent.children:
                    try:
                        del neighbour.neighbours[child]
                    except KeyError:
                        pass
                    if neighbour.add_neighbour(parent):
                        neighbour.score_all_neighbours(self.x, self.y, self.z, neighbours=[parent])
            # Disconnect the child from the tree completely
            child.parent = None
            child.neighbours = {}
            child.active = 3
            self.active_leaves.remove(child)
        # Adjust parent parameters to reflect new situation
        parent.children = []
        # During the run, neighbours are only pointing to voxels of the same or bigger size,
        # hence parent.neighbours is the same

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
        for leaf in self.active_leaves:
            leaf.set_neighbours()
            leaf.score_all_neighbours(self.x, self.y, self.z)

    def refine(self, min_side=100, max_side=10000):
        self.first_split()

        # Enforce all voxels to be smaller than the max_side given, without caring about connections
        while self.active_leaves[0].edge > max_side:
            self.split_active()
            self.set_contents()
            self.remove_empty_voxels()

            for leaf in self.active_leaves:
                leaf.set_neighbours()
                leaf.score_all_neighbours(self.x, self.y, self.z)
                leaf.set_label()

        # Look for endpoints and disconnected voxels in the active leaves, which are simply all non-empty voxels
        lonely = []
        for leaf in self.active_leaves:
            if leaf.label == 1:
                self.endpoints.append(leaf)
            elif leaf.label == 0:
                lonely.append(leaf)
        for lonely_leaf in lonely:
            lonely_leaf.active = "lonely"
            self.active_leaves.remove(lonely_leaf)

        # Once all voxels are of the required size, keep cutting carefully
        while len(self.active_leaves) > 0 and self.active_leaves[0].edge > min_side:
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
                leaf.score_all_neighbours(self.x, self.y, self.z)
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

        # After the loop, all leaves should be updated to have only leaf neighbours
        final_voxels = self.set_final_neighbours()
        for final_leaf in final_voxels:
            if len(final_leaf.neighbours) == 0:
                lonely.append(final_leaf)

        return lonely

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
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        import matplotlib.cm as cm

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
            if leaf.label == 0:
                plot_cube(ax1, leaf.center, leaf.edge, color="black")
            elif leaf.label == 1:
                plot_cube(ax1, leaf.center, leaf.edge, color="r")
            elif leaf.label == 3:
                plot_cube(ax1, leaf.center, leaf.edge, color="g")
            else:
                plot_cube(ax1, leaf.center, leaf.edge, color="b")

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()

    def make_voxel_graph(self, filename: str, max_score=500, c_map="inferno"):
        from graphviz import Graph
        from matplotlib import cm
        from matplotlib.colors import rgb_to_hsv

        # Make the graph and the list of all leaf voxels
        graph = Graph(comment='The voxel structure', filename='Graph_'+filename, format='png')
        voxels = self.find_leaves(self.root)
        colormap = cm.get_cmap(c_map)

        for counter in range(len(voxels)):
            # Make a node for every voxel, with the size depending on the number of data points inside it
            size = len(voxels[counter].contents)
            graph.node('voxel' + str(counter), label=None, shape='point', fixedsize='true', width=str(0.05 * size))

        for counter in range(len(voxels)):
            # Draw for every node the edges corresponding to the neighbours
            nn = voxels[counter].neighbours

            # Limit the number of drawn neighbours
            if len(nn) > 3:
                top_nn = dict(sorted(nn.items(), key=lambda k: k[1][1])[:3])
            else:
                top_nn = nn

            # Change the drawing style and color depending on the type and score respectively
            for neighbour in top_nn:
                pointer = voxels.index(neighbour)
                ninfo = top_nn[neighbour]
                if ninfo[0] == 'face':
                    linestyle = 'solid'
                elif ninfo[0] == 'edge':
                    linestyle = 'dashed'
                else:
                    linestyle = 'dotted'

                if ninfo[1] > max_score:
                    print(f"Max score has been exceeded with {ninfo[1]}")
                    score = max_score
                else:
                    score = ninfo[1]
                norm = score / max_score
                color = rgb_to_hsv(colormap(norm)[0:3])
                graph.edge('voxel' + str(counter), 'voxel' + str(pointer), style=linestyle,
                           color=f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f}")

        # Render the graph and save it
        graph.render()
