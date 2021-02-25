from anytree import NodeMixin, RenderTree
from anytree.search import findall_by_attr
from Lightcone_approach.Lightcone_search_one_direction import Tracker
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import pickle

LIST_OF_COLORS = ['#153e90', '#54e346', '#581845', '#825959', '#89937f', '#0e49b5', '#4e89ae', '#f1fa3c',
                  '#e28316', '#43658b', '#aa26da', '#fa163f', '#898d90', '#fa26a0', '#05dfd7', '#a3f7bf',
                  '#d68060', '#532e1c', '#59886b', '#db6400']


class Source:
    def __init__(self, x, y, z, t, ID):
        """
        Wrapper for a lightning VHF source.
        :param x: x-coordinate of the source.
        :param y: y-coordinate of the source.
        :param z: z-coordinate of the source.
        :param t: t-coordinate of the source.
        :param ID: Unique identifier of the source, for bookkeeping purposes.
        """
        self.position = np.array([x, y, z])
        self.t = t
        self.ID = ID
        self.selected = False
        self.branch = None


class ListNode(list, NodeMixin):
    def __init__(self, name, lst=None, parent=None, children=None):
        """
        Custom node structure to collect all sources of a branch. Has all the functionality to be used with a tree data
        structure.
        :param name: Unique name of the node.
        :param lst: List of the sources.
        :param parent: Parent branch, must also be a ListNode.
        :param children: Children branches, must also be ListNodes.
        """
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
    def __init__(self, x, y, z, t, direction, weights=(1, 0), d_cut=700, max_points=1000, max_branch=100):
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
        txyz = sorted(zip(t, x, y, z))
        t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
        self.tracker = Tracker(x_sorted, y_sorted, z_sorted, t_sorted, -1, weights, d_cut, direction, max_points)
        self.sources = [Source(a, b, c, d, idx) for (d, a, b, c), idx in zip(txyz, range(len(txyz)))]
        self.direction = direction
        self.tree = ListNode('root')
        self.lonely = ListNode('lonely')
        self.labelling = True
        self.counter = 0
        self.max_branch = max_branch

    def render_tree(self):
        """
        Render the internal tree
        """
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
        for _, _, node in RenderTree(self.tree.children[0]):
            color = mcolors.hex2color(LIST_OF_COLORS[int(counter % len(LIST_OF_COLORS))])
            ax2.scatter([x_plot[ind] for ind in node], [y_plot[ind] for ind in node], [z_plot[ind] for ind in node],
                        color=color, marker='o')
            ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')
            counter += 1

        for _, _, node in RenderTree(self.lonely):
            ax2.scatter([x_plot[ind] for ind in node], [y_plot[ind] for ind in node],
                        [z_plot[ind] for ind in node], color='k', marker='s')
            if node.name == 'lonely':
                continue
            ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()

    def plot_FT(self):
        fig = plt.figure(2, figsize=(20, 10))

        x_plot = self.tracker.x
        y_plot = self.tracker.y
        z_plot = self.tracker.z
        t_plot = self.tracker.t

        grid = np.array([t_plot, x_plot, y_plot, z_plot])
        fgrid = np.fft.fftn(grid)
        ft = fgrid[0, :]
        fx = fgrid[1, :]
        fy = fgrid[2, :]
        fz = fgrid[3, :]

        cmap = cm.plasma
        norm = mcolors.Normalize(vmin=min(abs(ft)), vmax=max(abs(ft)))

        ax1 = fig.add_subplot(121, projection='3d', xlim=[0, 1e5], ylim=[0, 5e4])
        ax1.scatter(abs(fx), abs(fy), abs(fz), marker='^', c=abs(ft), cmap=cmap, norm=norm)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('FT of the original data')

        ax2 = fig.add_subplot(122, projection='3d', xlim=[0, 1e5], ylim=[0, 5e4])
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('FT of each branch')

        counter = 0
        for _, _, node in RenderTree(self.tree.children[0]):
            color = mcolors.hex2color(LIST_OF_COLORS[int(counter % len(LIST_OF_COLORS))])
            x = [x_plot[ind] for ind in node]
            y = [y_plot[ind] for ind in node]
            z = [z_plot[ind] for ind in node]
            t = [t_plot[ind] for ind in node]

            grid2 = np.array([t, x, y, z])
            fgrid2 = np.fft.fftn(grid2)
            ft2 = fgrid2[0, :]
            fx2 = fgrid2[1, :]
            fy2 = fgrid2[2, :]
            fz2 = fgrid2[3, :]

            ax2.scatter(abs(fx2), abs(fy2), abs(fz2), color=color, marker='o')
            ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')
            counter += 1

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()

    def identify_data(self, branch=0):
        x_plot = self.tracker.x
        y_plot = self.tracker.y
        z_plot = self.tracker.z
        t_plot = self.tracker.t

        if branch == 0:
            x = x_plot
            y = y_plot
            z = z_plot
            t = t_plot
        else:
            node = findall_by_attr(self.tree, 'n'+str(branch))
            x = [x_plot[ind] for ind in node[0]]
            y = [y_plot[ind] for ind in node[0]]
            z = [z_plot[ind] for ind in node[0]]
            t = [t_plot[ind] for ind in node[0]]

        cmap = cm.plasma
        norm = mcolors.Normalize(vmin=t[0], vmax=t[-1])

        fig, ax = plt.subplots(2, 2, figsize=(10, 10))

        ax[0, 0].scatter(t, z, marker='o', c=t, cmap=cmap, norm=norm)
        ax[0, 0].set_xlabel('Time [s]')
        ax[0, 0].set_ylabel('Height [m]')

        ax[0, 1].scatter(x, y, marker='o', c=t, cmap=cmap, norm=norm)
        ax[0, 1].set_xlabel('Easting [m]')
        ax[0, 1].set_ylabel('Northing [m]')

        ax[1, 0].scatter(t, x, marker='o', c=t, cmap=cmap, norm=norm)
        ax[1, 0].set_xlabel('Time [s]')
        ax[1, 0].set_ylabel('Easting [m]')

        ax[1, 1].scatter(t, y, marker='o', c=t, cmap=cmap, norm=norm)
        ax[1, 1].set_xlabel('Time [s]')
        ax[1, 1].set_ylabel('Northing [m]')

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
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
        rest_node = ListNode('n' + str(self.counter), rest, parent=branch)
        self.counter += 1
        for idx in rest:
            self.sources[idx].branch = rest_node
        insert_node = ListNode('n' + str(self.counter), leaf, parent=branch)
        self.counter += 1
        for idx in leaf:
            self.sources[idx].selected = True
            self.sources[idx].branch = insert_node

    def merge_branch(self, branch: ListNode, new_part: list):
        branch.extend(new_part)
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
            self.merge_branch(insertion_source.branch, new_branch)
            self.labelling = True
        else:
            self.labelling = False

    def label(self):
        self.first_branch()
        while self.labelling:
            self.find_next_branch()
            if self.counter >= self.max_branch:
                break

    def save_tree_to_file(self, file):
        f = open('Pickle_saves/' + file, 'wb')
        pickle.dump(self.tree, f)

    def load_tree_from_file(self, file):
        f = open('Pickle_saves/' + file, 'rb')
        self.tree = pickle.load(f)
