"""
TODO: How to count neighbours of Voxel?
"""

import numpy as np


class Voxel:
    def __init__(self, center: np.array, edge, parent=None):
        self.center = center
        self.edge = edge
        self.parent = parent
        self.children = [None] * 8
        self._set_contents()

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


class Octree:
    def __init__(self, t, x, y, z):
        txyz = sorted(zip(t, x, y, z))
        self.t, self.x, self.y, self.z = map(np.array, zip(*list(txyz)))

        center = np.array([(x.min() + x.max()) / 2, (y.min() + y.max()) / 2, (z.min() + z.max()) / 2])
        longest_side = np.max([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()])

        self.root = Voxel(center, longest_side)
        self.root.contents = list(range(len(self.t)))

        self.leaves = []

    def neighbours(self, voxel):
        return voxel

    def count_neighbours(self):
        count = []
        for voxel in self.leaves:
            neighbours = self.neighbours(voxel)
            count.append(len(neighbours))

        return count

    def first_split(self):
        self.root.split()
        self.leaves.extend(self.root.children)

    def refine_local(self):
        count = self.count_neighbours()
        cont = False

        for ind in range(len(count)):
            if count[ind] > 3:
                cont = True
                self.leaves[ind].split()

        return cont

    def refine(self):
        self.first_split()

        cont = True
        while cont:
            cont = self.refine_local()
