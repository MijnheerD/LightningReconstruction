"""

"""

from Analyzer_template import LightningReconstructor, ListNode
from Mesh_octree import Octree, Voxel


class Analyzer(LightningReconstructor):
    def __init__(self, t, x, y, z, min_voxel_size=100, max_voxel_size=10000, max_branch=100):
        super().__init__(max_branch)

        self.octree = Octree(t, x, y, z)
        self.min_voxel_size = min_voxel_size
        self.max_voxel_size = max_voxel_size

    def get_x(self):
        return self.octree.x

    def get_y(self):
        return self.octree.y

    def get_z(self):
        return self.octree.z

    def get_t(self):
        return self.octree.t

    def find_begin_voxel(self):
        minimum = 1000
        minimum_leaf = None
        for leaf in self.octree.endpoints:
            if min(leaf.contents) < minimum:
                minimum = min(leaf.contents)
                minimum_leaf = leaf
                if minimum == 0:
                    break
        return minimum_leaf

    def find_next_voxel(self, voxel: Voxel):
        # start_time = voxel.contents[-1]

        next_counter = 0
        nextBP = voxel.neighbours[next_counter]
        while nextBP.selected:  # or (nextBP.contents[0] < start_time):
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
        self.lonely.extend(self.octree.refine(min_side=self.min_voxel_size, max_side=self.max_voxel_size))
        start = self.find_begin_voxel()

        start.selected = True
        pool, BP = self.find_branch(start)
        new_node = ListNode('n' + str(self.counter), pool, parent=self.tree)
        self.counter += 1

        if BP is not None:
            self.insert_branch(BP, new_node)
