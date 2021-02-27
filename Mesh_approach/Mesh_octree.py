"""
TODO: Implement add neighbour of voxel
"""

import numpy as np


class Voxel:
    def __init__(self, center: np.array, edge, parent=None):
        self.center = center
        self.edge = edge
        self.parent = parent
        self.neighbours = []
        self.children = []

        self._set_contents()

    def remove_child(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            print(f'The voxel{child} is not a child of {self}')

    def _set_contents(self):
        if self.parent is not None:
            xmin = self.parent.contents > (self.center[0] - self.edge / 2)
            xmax = self.parent.contents < (self.center[0] + self.edge / 2)

            ymin = self.parent.contents > (self.center[1] - self.edge / 2)
            ymax = self.parent.contents < (self.center[1] + self.edge / 2)

            zmin = self.parent.contents > (self.center[2] - self.edge / 2)
            zmax = self.parent.contents < (self.center[2] + self.edge / 2)

            self.contents = xmin*xmax*ymin*ymax*zmin*zmax
        else:
            self.contents = []

    def _is_neighbour(self, other):
        return (other.edge + self.edge) / np.sqrt(2) <= np.linalg.norm(other.center - self.center)

    def look_for_neighbours(self, possible_neighbours):
        for neighbour in possible_neighbours:
            if len(neighbour.children) == 0:
                if self._is_neighbour(neighbour):
                    self.neighbours.append(neighbour)
            else:
                for child in neighbour.children:
                    self.look_for_neighbours(child.neighbours)

    def split(self):
        new_length = self.edge / 2

        self.children = [
            Voxel(self.center + np.array([new_length / 2, new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([new_length / 2, new_length / 2, -new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([new_length / 2, -new_length / 2, -new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([new_length / 2, -new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, -new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, new_length / 2, new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, new_length / 2, -new_length / 2]), new_length, parent=self),
            Voxel(self.center + np.array([-new_length / 2, -new_length / 2, -new_length / 2]), new_length, parent=self)]

        for child in self.children:
            child.neighbours.extend(self.children)
            child.neighbours.remove(child)

            child.look_for_neighbours(self.neighbours)

        return self.children


class Octree:
    def __init__(self, t, x, y, z):
        txyz = sorted(zip(t, x, y, z))
        self.t, self.x, self.y, self.z = map(np.array, zip(*list(txyz)))

        center = np.array([(x.min() + x.max()) / 2, (y.min() + y.max()) / 2, (z.min() + z.max()) / 2])
        longest_side = np.max([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()])

        self.root = Voxel(center, longest_side)
        self.root.contents = list(range(len(self.t)))

        self.leaves = []

    def count_neighbours(self):
        count = []
        for voxel in self.leaves:
            count.append(len(voxel.neighbours))

        return count

    def remove_empty_voxels(self):
        for leaf in self.leaves:
            if len(leaf.contents) == 0:
                leaf.parent.remove_child(leaf)
                self.leaves.remove(leaf)
                del leaf

    def first_split(self):
        children = self.root.split()
        self.leaves.extend(children)
        self.remove_empty_voxels()

    def refine_local(self):
        count = self.count_neighbours()
        cont = False
        new_leaves = []

        for ind in range(len(count)):
            if count[ind] > 3:
                cont = True
                children = self.leaves[ind].split()
                new_leaves.extend(children)

        self.leaves = new_leaves

        return cont

    def refine(self):
        self.first_split()

        cont = True
        while cont:
            cont = self.refine_local()
            self.remove_empty_voxels()
