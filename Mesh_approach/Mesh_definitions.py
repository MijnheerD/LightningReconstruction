"""
TODO: make remove_neighbour recursive
TODO: distribute contents over children
TODO: add_neighbour does not work correctly when neighbours are already split
"""
import numpy as np


def recursive_len(item):
    if type(item) == list:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


class Voxel:
    def __init__(self, center: np.array, edge):
        self.center = center
        self.edge = edge
        self.neighbours = [None]*26
        self.contents = []

    def _split_self(self):
        assert len(self.contents) > 1, "Voxel has only 1 element left"

        new_length = self.edge / 2

        child0 = Voxel(self.center + np.array([new_length / 2, new_length / 2, new_length / 2]), new_length)
        child1 = Voxel(self.center + np.array([new_length / 2, new_length / 2, -new_length / 2]), new_length)
        child2 = Voxel(self.center + np.array([new_length / 2, -new_length / 2, -new_length / 2]), new_length)
        child3 = Voxel(self.center + np.array([new_length / 2, -new_length / 2, new_length / 2]), new_length)
        child4 = Voxel(self.center + np.array([-new_length / 2, -new_length / 2, new_length / 2]), new_length)
        child5 = Voxel(self.center + np.array([-new_length / 2, new_length / 2, new_length / 2]), new_length)
        child6 = Voxel(self.center + np.array([-new_length / 2, new_length / 2, -new_length / 2]), new_length)
        child7 = Voxel(self.center + np.array([-new_length / 2, -new_length / 2, -new_length / 2]), new_length)

        child0.add_neighbour(child1, 17)
        child0.add_neighbour(child2, 18)
        child0.add_neighbour(child3, 0)
        child0.add_neighbour(child4, 16)
        child0.add_neighbour(child5, 15)
        child0.add_neighbour(child6, 24)
        child0.add_neighbour(child7, 25)

        child1.add_neighbour(child2, 0)
        child1.add_neighbour(child3, 4)
        child1.add_neighbour(child4, 5)
        child1.add_neighbour(child5, 6)
        child1.add_neighbour(child6, 15)
        child1.add_neighbour(child7, 16)

        child2.add_neighbour(child3, 9)
        child2.add_neighbour(child4, 6)
        child2.add_neighbour(child5, 7)
        child2.add_neighbour(child6, 11)
        child2.add_neighbour(child7, 15)

        child3.add_neighbour(child4, 15)
        child3.add_neighbour(child5, 11)
        child3.add_neighbour(child6, 23)
        child3.add_neighbour(child7, 24)

        child4.add_neighbour(child5, 13)
        child4.add_neighbour(child6, 22)
        child4.add_neighbour(child7, 17)

        child5.add_neighbour(child6, 17)
        child5.add_neighbour(child7, 18)

        child6.add_neighbour(child7, 0)

        for idx in range(26):
            for child in [child0, child1, child2, child3, child4, child5, child6, child7]:
                if child.neighbours[idx] is None:
                    child.add_neighbour(self.neighbours[idx], idx)

        del self

    def nr_of_datapoints(self):
        return len(self.contents)

    def nr_of_active_neighbours(self):
        return recursive_len(self.neighbours)

    def add_neighbour(self, neighbour, index):
        """
        Adding a neighbour overwrites the neighbour in the list, but appends to the other one.
        :param neighbour:
        :param index:
        :return:
        """
        self.neighbours[index] = neighbour

        if neighbour is None:
            return

        if index == 13:
            n_index = 0
        elif index == 0:
            n_index = 13
        else:
            n_index = int(26-index)

        if neighbour.neighbours[n_index] is None:
            neighbour.neighbours[n_index] = self
        else:
            neighbour.neighbours[n_index] = list(neighbour.neighbours[n_index]).append(self)

    def remove_neighbour(self, neighbour):
        self.neighbours.remove(neighbour)

    def __del__(self):
        for neighbour in self.neighbours:
            if neighbour is not None:
                neighbour.remove_neighbour(self)
