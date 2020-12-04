"""
TODO: rewrite first_branch(), to make it search whole source space
"""

from anytree import NodeMixin, RenderTree
from Lightcone_approach.Lightcone_search_one_direction import Tracker
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm


LIST_OF_COLORS = ['#ffa372', '#ed6663', '#43658b', '#4e89ae', '#fa26a0', '#05dfd7', '#a3f7bf', '#fff591']


class Source:
    def __init__(self, x, y, z, t, ID):
        self.position = np.array([x, y, z])
        self.t = t
        self.ID = ID
        self.selected = False
        self.branch = None


class ListNode(list, NodeMixin):
    def __init__(self, name, lst=None, parent=None, children=None):
        if lst is None:
            lst = []
        super().__init__(lst)
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def update(self, contents: list):
        self.clear()
        self.extend(contents)


class Analyzer:
    def __init__(self, x, y, z, t, direction, weights=(1, 0), d_cut=700, max_points=200, max_branch=100):
        # Sort the data by time
        txyz = sorted(zip(t, x, y, z))
        t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
        self.tracker = Tracker(x_sorted, y_sorted, z_sorted, t_sorted, -1, weights, d_cut, direction, max_points)
        self.sources = [Source(a, b, c, d, idx) for (d, a, b, c), idx in zip(txyz, range(len(txyz)))]
        self.direction = direction
        self.tree = ListNode('root')
        self.labelling = True
        self.counter = 0
        self.max_branch = max_branch

    def render_tree(self):
        for pre, _, node in RenderTree(self.tree):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), len(node))

    def plot_tree(self):
        fig = plt.figure(1, figsize=(20, 10))

        x_plot = self.tracker.x
        y_plot = self.tracker.y
        z_plot = self.tracker.z
        t_plot = self.tracker.t

        cmap = cm.plasma
        norm = mcolors.Normalize(vmin=t_plot[0], vmax=t_plot[-1])

        ax1 = fig.add_subplot(121, projection='3d')
        ax1.scatter(x_plot, y_plot, z_plot, marker='^', c=t_plot, cmap=cmap, norm=norm)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('Time ordered original data')

        ax2 = fig.add_subplot(122, projection='3d')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('Branches selected by the algorithm')
        (left, right) = ax1.get_xlim3d()
        ax2.set_xlim3d(left, right)
        (left, right) = ax1.get_ylim3d()
        ax2.set_ylim3d(left, right)
        (left, right) = ax1.get_zlim3d()
        ax2.set_zlim3d(left, right)

        counter = 0
        for _, _, node in RenderTree(self.tree):
            color = mcolors.hex2color(LIST_OF_COLORS[int(counter % len(LIST_OF_COLORS))])
            ax2.scatter([x_plot[ind] for ind in node], [y_plot[ind] for ind in node], [z_plot[ind] for ind in node],
                        color=color, marker='o')
            counter += 1

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()

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
        for idx in leaf:
            self.sources[idx].selected = True
            self.sources[idx].branch = insert_node
        rest_node = ListNode('n'+str(self.counter), rest, parent=branch)
        self.counter += 1
        for idx in rest:
            self.sources[idx].branch = rest_node

    def merge_branch(self, branch: ListNode, new_part: list):
        branch.extend(new_part[:-1])
        for idx in new_part:
            self.sources[idx].selected = True
            self.sources[idx].branch = branch

    def next_seed(self):
        idx = -1
        source = self.sources[idx]
        while source.selected:
            if idx == -len(self.sources):
                self.labelling = False
                return None
            idx -= 1
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
        self.tracker.first_step()
        seed_added = -1
        while self.tracker.search:
            seed_added = self.tracker.find_next()
            if self.sources[seed_added].selected or len(self.tracker.pool) > self.tracker.max_points:
                break

        pool = list(self.tracker.pool)
        insertion_source = self.sources[seed_added]
        if len(pool) >= 10:
            self.insert_branch(insertion_source.branch, seed_added, pool)
            self.labelling = True
        elif len(pool) > 0:
            self.merge_branch(insertion_source.branch, pool)
            self.labelling = True
        else:
            self.labelling = False

    def label(self):
        self.first_branch()
        while self.labelling:
            self.find_next_branch()
            if self.counter >= self.max_branch:
                break
