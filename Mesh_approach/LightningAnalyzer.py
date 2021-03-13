"""
TODO: make branch reconstructor start at endpoint with earliest time
"""

from Analyzer_template import LightningReconstructor, ListNode
from Mesh_octree import Octree, Voxel


class Analyzer(LightningReconstructor):
    def __init__(self, t, x, y, z, min_voxel_size=100, max_voxel_size=10000, max_branch=100):
        super().__init__()

        self.octree = Octree(t, x, y, z)
        self.labelling = True
        self.counter = 0
        self.min_voxel_size = min_voxel_size
        self.max_voxel_size = max_voxel_size
        self.max_branch = max_branch

    def plot_tree(self):
        x_plot = self.octree.x
        y_plot = self.octree.y
        z_plot = self.octree.z
        t_plot = self.octree.t

        super()._plot_tree(t_plot, x_plot, y_plot, z_plot)

    def plot_FT(self):
        x_plot = self.octree.x
        y_plot = self.octree.y
        z_plot = self.octree.z
        t_plot = self.octree.t

        super()._plot_FT(t_plot, x_plot, y_plot, z_plot)

    def identify_data(self, branch=0):
        x_plot = self.octree.x
        y_plot = self.octree.y
        z_plot = self.octree.z
        t_plot = self.octree.t

        super()._identify_data(t_plot, x_plot, y_plot, z_plot, branch)

    def line_plot(self):
        t_plot = self.octree.t

        super()._line_plot(t_plot)

    def find_earliest_voxel(self):
        leaves = self.octree.find_leaves(self.octree.root)
        for leaf in leaves:
            if 0 in leaf.contents:
                return leaf

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
        start = self.octree.endpoints[0]

        start.selected = True
        pool, BP = self.find_branch(start)
        new_node = ListNode('n' + str(self.counter), pool, parent=self.tree)
        self.counter += 1

        if BP is not None:
            self.insert_branch(BP, new_node)
