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


class Analyzer:
    def __init__(self, x, y, z, t, seed, direction, weights=(1, 0), d_cut=700, max_points=200):
        # Sort the data by time
        txyz = sorted(zip(t, x, y, z))
        self.sources = [Source(a, b, c, d, idx) for (d, a, b, c), idx in zip(txyz, range(len(txyz)))]
        self.direction = direction
        self.tree = ListNode('root')
        self.labelling = True

    def render_tree(self):
        for pre, _, node in RenderTree(self.tree):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), len(node))

    def first_branch(self):
        seed_source = self.sources[-1]
        x = np.array([seed_source.position[0]])
        y = np.array([seed_source.position[1]])
        z = np.array([seed_source.position[2]])
        t = np.array([seed_source.t])
        for idx in range(2, 20):
            pos = self.sources[-idx].position
            x = np.append(pos[0], x)
            y = np.append(pos[1], y)
            z = np.append(pos[2], z)
            t = np.append(self.sources[-idx].t, t)

        search = Tracker(x, y, z, t, len(t)-1, direction=self.direction)
        search.run()

        pool = []
        for i in search.pool:
            idx_in_sources_list = i-len(t)+1
            self.sources[idx_in_sources_list].selected = True
            pool.append(idx_in_sources_list)
        new_node = ListNode('n0', pool, parent=self.tree)

    def label(self):
        self.first_branch()
