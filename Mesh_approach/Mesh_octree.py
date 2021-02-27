"""

"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations, product


def plot_cube(ax, center, side_length):
    '''
    From https://stackoverflow.com/questions/11140163/plotting-a-3d-cube-a-sphere-and-a-vector-in-matplotlib#11156353
    :param ax:
    :param center:
    :param side_length:
    :return:
    '''
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

    def remove_child(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            print(f'The voxel{child} is not a child of {self}')

    def _set_contents(self, contents=None):
        if contents is not None:
            self.contents = contents
        else:
            pass

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
        self.root._set_contents(np.array(range(len(self.t))))

        self.active_leaves = []

    def set_contents(self, voxel: Voxel):
        if voxel.parent is not None:
            xmin = self.x[voxel.parent.contents] > (voxel.center[0] - voxel.edge / 2)
            xmax = self.x[voxel.parent.contents] < (voxel.center[0] + voxel.edge / 2)

            ymin = self.y[voxel.parent.contents] > (voxel.center[1] - voxel.edge / 2)
            ymax = self.y[voxel.parent.contents] < (voxel.center[1] + voxel.edge / 2)

            zmin = self.z[voxel.parent.contents] > (voxel.center[2] - voxel.edge / 2)
            zmax = self.z[voxel.parent.contents] < (voxel.center[2] + voxel.edge / 2)

            voxel._set_contents(voxel.parent.contents[xmin*xmax*ymin*ymax*zmin*zmax])
        else:
            voxel._set_contents()

    def count_neighbours(self):
        count = []
        for voxel in self.active_leaves:
            count.append(len(voxel.neighbours))

        return count

    def remove_empty_voxels(self):
        active_leaves = []
        for leaf in self.active_leaves:
            if len(leaf.contents) == 0:
                leaf.parent.remove_child(leaf)
            else:
                active_leaves.append(leaf)
        self.active_leaves = active_leaves

    def first_split(self):
        children = self.root.split()
        self.active_leaves.extend(children)
        for child in children:
            self.set_contents(child)

        self.remove_empty_voxels()
        for leaf in self.active_leaves:
            leaf.set_neighbours()

    def refine_local(self):
        count = self.count_neighbours()
        print(f'Counting is {count}')
        cont = False
        new_leaves = []

        for ind in range(len(count)):
            if count[ind] > 3:
                cont = True
                children = self.active_leaves[ind].split()
                new_leaves.extend(children)
                for child in children:
                    self.set_contents(child)

        self.active_leaves = new_leaves

        return cont

    def refine(self):
        self.first_split()

        cont = True
        while cont:
            cont = self.refine_local()

            self.remove_empty_voxels()
            for leaf in self.active_leaves:
                leaf.set_neighbours()

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

        ax1.scatter(self.x, self.y, self.z, marker='x', c=self.t)
        for leaf in leaves:
            # print(f"Leaf has its center at {leaf.center} with edge length {leaf.edge}")
            plot_cube(ax1, leaf.center, leaf.edge)

        plt.show()
