'''
TODO: rewrite first_branch(), to make it search whole source space
'''

from anytree import NodeMixin, RenderTree
from Lightcone_approach.Lightcone_search_one_direction import Tracker
import numpy as np


class Source:
    def __init__(self, x, y, z, t, ID):
        self.position = np.array([x, y, z])
        self.t = t
        self.ID = ID
        self.selected = False
        self.branch = None


class ListNode(list, NodeMixin):
    def __init__(self, name, lst=[], parent=None, children=None):
        super().__init__(lst)
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def update(self, contents: list):
        self.clear()
        self.extend(contents)


class Analyzer:
    def __init__(self, x, y, z, t, direction, weights=(1, 0), d_cut=700, max_points=200):
        # Sort the data by time
        txyz = sorted(zip(t, x, y, z))
        t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
        self.tracker = Tracker(x_sorted, y_sorted, z_sorted, t_sorted, -1, weights, d_cut, direction, max_points)
        self.sources = [Source(a, b, c, d, idx) for (d, a, b, c), idx in zip(txyz, range(len(txyz)))]
        self.direction = direction
        self.tree = ListNode('root')
        self.labelling = True
        self.counter = 0

    def render_tree(self):
        for pre, _, node in RenderTree(self.tree):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), len(node))

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

        branch.update(root)
        insert_node = ListNode('n'+str(self.counter), leaf, parent=branch)
        self.counter += 1
        rest_node = ListNode('n'+str(self.counter), rest, parent=branch)
        self.counter += 1

    def merge_branch(self, branch: ListNode, new_part: list):
        branch.extend(new_part)

    def next_seed(self):
        idx = -1
        source = self.sources[idx]
        while source.selected:
            idx -= 1
            source = self.sources[idx]
        return source.ID

    def find_next_branch(self):
        self.labelling = False

        seed_source = self.sources[self.next_seed()]
        self.tracker.reset_to_seed(seed_source.ID)

        # Run the tracker, but check in every step if we encounter an already selected source
        self.tracker.first_step()
        while self.tracker.search:
            seed_added = self.tracker.find_next()
            if self.sources[seed_added].selected or len(self.tracker.pool) > self.tracker.max_points:
                break

        pool = list(self.tracker.pool)
        insertion_source = self.sources[seed_added]
        if len(pool) > 10:
            self.insert_branch(insertion_source.branch, seed_added, pool)
            self.labelling = True
        elif len(pool) > 0:
            self.merge_branch(insertion_source.branch, pool)
            self.labelling = True

    def label(self):
        self.first_branch()
        while self.labelling:
            self.render_tree()
            self.find_next_branch()
