"""

"""

import numpy as np
from Analyzer_template import LightningReconstructor, ListNode
from Lightcone_approach.Lightcone_search_one_direction import Tracker, Source


class Analyzer (LightningReconstructor):
    def __init__(self, t, x, y, z, direction, weights=(1, 0), d_cut=700, max_points=1000, max_branch=100):
        """
        Class to analyze a lightning flash and divide the data into labelled branches. The result is stored inside a
        tree structure, in which every node contains the list of identifiers of the sources inside that branch. Note
        that the indices might not be sorted by time.
        :param x: Array of the x-coordinates of the data to analyze (easting).
        :param y: Array of the y-coordinates of the data to analyze (northing).
        :param z: Array of the z-coordinates of the data to analyze (height).
        :param t: Array of the t-coordinates of the data to analyze.
        :param direction: Direction of time in which to search (-1: backwards, 1: forwards).
        :param weights: Weights to be used in the search for the next point inside a branch.
        :param d_cut: Max distance between points that can be connected inside the same branch.
        :param max_points: Max number of points a branch can contain.
        :param max_branch: Max number of branches the analyzer may label.
        """
        super().__init__(max_branch, 'Lightcone')

        txyz = sorted(zip(t, x, y, z))
        t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
        self.tracker = Tracker(x_sorted, y_sorted, z_sorted, t_sorted, -1, weights, d_cut, direction, max_points)
        self.sources = [Source(a, b, c, d, idx) for (d, a, b, c), idx in zip(txyz, range(len(txyz)))]
        self.direction = direction

    def get_x(self):
        return self.tracker.x

    def get_y(self):
        return self.tracker.y

    def get_z(self):
        return self.tracker.z

    def get_t(self):
        return self.tracker.t

    def first_branch(self):
        seed_source = self.sources[-1]

        self.tracker.reset_to_seed(seed_source.ID)
        self.tracker.run()

        pool = list(self.tracker.pool)
        new_node = ListNode('n0', pool, parent=self.tree)
        self.counter += 1
        for idx in pool:
            self.sources[idx].selected = True
            self.sources[idx].branch = new_node

    def insert_branch(self, branch: ListNode, insertion_id: int, leaf: list):
        insertion_index = branch.index(insertion_id)
        root = branch[:insertion_index + 1]
        rest = branch[insertion_index + 1:]

        if len(rest) < 10:
            # If the insertion would result in a too small branch, do not split
            branch.extend(leaf)
            for idx in leaf:
                self.sources[idx].selected = True
                self.sources[idx].branch = branch
        else:
            # Create two new nodes and wire them to the parent branch
            branch.update(root)
            ex_children = branch.children

            rest_node = ListNode('n' + str(self.counter), rest, parent=branch)
            self.counter += 1
            for idx in rest:
                self.sources[idx].branch = rest_node

            insert_node = ListNode('n' + str(self.counter), leaf, parent=branch)
            self.counter += 1
            for idx in leaf:
                self.sources[idx].selected = True
                self.sources[idx].branch = insert_node

            # Rewire the parent-children relationship to reflect new situation
            for child in ex_children:
                child.parent = rest_node
            branch.set_children([rest_node, insert_node])

    def merge_branch(self, branch: ListNode, insertion_id: int, new_part: list):
        insertion_index = branch.index(insertion_id)
        for i in range(len(new_part)):
            branch.insert(i + insertion_index, new_part[i])
        for idx in new_part:
            self.sources[idx].selected = True
            self.sources[idx].branch = branch

    def next_seed(self):
        idx = self.direction
        source = self.sources[idx]
        while source.selected:
            if abs(idx) == len(self.sources):
                self.labelling = False
                return None
            idx += self.direction
            source = self.sources[idx]
        return source.ID

    def find_next_branch(self):
        seed = self.next_seed()
        if seed is not None:
            seed_source = self.sources[seed]
        else:
            return
        self.tracker.reset_to_seed(seed_source.ID)

        # Run the tracker, but check in every step if we encounter an already selected source
        seed_added = self.tracker.first_step()
        while self.tracker.search:
            if self.sources[seed_added].selected or len(self.tracker.pool) > self.tracker.max_points:
                break
            seed_added = self.tracker.find_next()

        pool = list(self.tracker.pool)
        if seed_added is None:
            if len(pool) > 1:
                node = ListNode('L', pool, parent=self.lonely)
            else:
                self.lonely.extend(pool)
                node = self.lonely
            for idx in pool:
                self.sources[idx].selected = True
                self.sources[idx].branch = node
            return

        insertion_source = self.sources[seed_added]
        # Pool most likely has an already selected source as its first/last element, depending on the direction
        if self.direction == 1:
            new_branch = pool[:-1]
        elif self.direction == -1:
            new_branch = pool[1:]
        else:
            raise ValueError('Direction is not valid')

        if len(pool) >= 10:
            self.insert_branch(insertion_source.branch, seed_added, new_branch)
            self.labelling = True
        elif len(pool) > 0:
            self.merge_branch(insertion_source.branch, seed_added, new_branch)
            self.labelling = True
        else:
            self.labelling = False

    def label(self):
        self.first_branch()
        while self.labelling:
            self.find_next_branch()
            if self.counter >= self.max_branch:
                break
