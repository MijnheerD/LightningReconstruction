"""
TODO: find solution for lonely points which get their own voxel
TODO: recover branches from final voxel configuration
TODO: implement tree structure to print/save
TODO: make general Analyzer class to inherit from (make full code packable)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from itertools import combinations, product


def plot_cube(ax, center, side_length):
    """
    From https://stackoverflow.com/questions/11140163/plotting-a-3d-cube-a-sphere-and-a-vector-in-matplotlib#11156353
    :param ax:
    :param center:
    :param side_length:
    :return:
    """
    r_x = [center[0] - side_length / 2, center[0] + side_length / 2]
    r_y = [center[1] - side_length / 2, center[1] + side_length / 2]
    r_z = [center[2] - side_length / 2, center[2] + side_length / 2]
    for s, e in combinations(np.array(list(product(r_x, r_y, r_z))), 2):
        if side_length+0.0001 >= np.sum(np.abs(s - e)) >= side_length-0.0001:
            ax.plot3D(*zip(s, e), color="b")


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

    def remove_child(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            print(f'The voxel{child} is not a child of {self}')

    def set_contents(self, contents=None):
        if contents is not None:
            self.contents = contents
        else:
            pass

    def set_label(self, modifier=0):
        """
        Set the label of the voxel.
        0 = split should be reverted
        1 = Endpoint
        2 = Branch
        3 = BP
        """
        if (len(self.neighbours) - modifier) < 4:
            self.label = len(self.neighbours)

    def check_neighbours(self):
        fake = 0
        for neighbour in self.neighbours:
            count = 0
            for nn in neighbour.neighbours:
                if nn not in self.neighbours:
                    count += 1
            if count == 0:
                fake += 1
        return fake

    def check_parent_relation(self):
        if self.label == 1:
            if self.parent.label != 1:
                return self

        if self.parent.label == 2:
            if self.label == 2:
                self.active = False
            elif self.label == 3:
                fake = self.check_neighbours()
                self.set_label(fake)
                self.check_parent_relation()

        if self.label is None:
            fake = self.check_neighbours()
            self.set_label(fake)
            self.check_parent_relation()

        return None

    def _is_neighbour(self, other):
        return (other.edge + self.edge) / np.sqrt(2) >= np.linalg.norm(other.center - self.center)

    def look_for_neighbours(self, possible_neighbours):
        for neighbour in possible_neighbours:
            if len(neighbour.children) == 0:
                if self._is_neighbour(neighbour):
                    self.neighbours.append(neighbour)
            else:
                self.look_for_neighbours(neighbour.children)

    def set_neighbours(self):
        self.neighbours.extend(self.parent.children)
        self.neighbours.remove(self)

        self.look_for_neighbours(self.parent.neighbours)

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


class Octree:
    def __init__(self, t, x, y, z):
        txyz = sorted(zip(t, x, y, z))
        self.t, self.x, self.y, self.z = map(np.array, zip(*list(txyz)))

        center = np.array([(x.min() + x.max()) / 2, (y.min() + y.max()) / 2, (z.min() + z.max()) / 2])
        longest_side = np.max([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()])

        self.root = Voxel(center, longest_side)
        self.root.set_contents(np.array(range(len(self.t))))

        self.active_leaves = []

    def set_contents(self, voxel: Voxel):
        if voxel.parent is not None:
            xmin = self.x[voxel.parent.contents] > (voxel.center[0] - voxel.edge / 2)
            xmax = self.x[voxel.parent.contents] < (voxel.center[0] + voxel.edge / 2)

            ymin = self.y[voxel.parent.contents] > (voxel.center[1] - voxel.edge / 2)
            ymax = self.y[voxel.parent.contents] < (voxel.center[1] + voxel.edge / 2)

            zmin = self.z[voxel.parent.contents] > (voxel.center[2] - voxel.edge / 2)
            zmax = self.z[voxel.parent.contents] < (voxel.center[2] + voxel.edge / 2)

            voxel.set_contents(voxel.parent.contents[xmin*xmax*ymin*ymax*zmin*zmax])
        else:
            voxel.set_contents()

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

    def split_active(self):
        """
        Split all the active voxels, with an extra check if they are active (should be able to ommit).
        """
        new_leaves = []
        for ind in range(len(self.active_leaves)):
            if self.active_leaves[ind].active:
                children = self.active_leaves[ind].split()
                new_leaves.extend(children)
        self.active_leaves = new_leaves

    def revert_split(self, parent: Voxel):
        parent.active = False
        for child in parent.children:
            child.parent = None
            self.active_leaves.remove(child)
        parent.children = []

    def first_split(self):
        children = self.root.split()
        self.active_leaves.extend(children)
        for child in children:
            self.set_contents(child)
            child.label = 1

        self.remove_empty_voxels()
        for leaf in self.active_leaves:
            leaf.set_neighbours()

    def refine(self):
        self.first_split()

        while len(self.active_leaves) > 0:
            # Print the number of neighbours of current active leaves
            self.count_neighbours()

            # Split every active voxel into 8 parts
            self.split_active()

            # Remove the empty voxels from the list
            self.remove_empty_voxels()

            # Set the neighbours for every voxel which is not empty and label them accordingly
            revert_parents = set()
            for leaf in self.active_leaves:
                leaf.set_neighbours()
                leaf.set_label()
                if leaf.label == 0:
                    revert_parents.add(leaf.parent)

            # Check if the voxels are still active: check neighbours and revert split if voxel is disconnected
            for parent in revert_parents:
                self.revert_split(parent)

            # Check if the voxels are still active: check relation with parent
            revert_parents.clear()
            for voxel in self.active_leaves:
                result = voxel.check_parent_relation()
                if result is not None:
                    revert_parents.add(result.parent)

    def find_leaves(self, voxel):
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
            plot_cube(ax1, leaf.center, leaf.edge)

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()
