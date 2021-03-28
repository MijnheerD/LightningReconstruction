import pickle
import numpy as np  # Only necessary for FT
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from anytree import NodeMixin, RenderTree, LevelGroupOrderIter
from anytree.search import findall_by_attr


LIST_OF_COLORS = ['#153e90', '#54e346', '#581845', '#825959', '#89937f', '#0e49b5', '#4e89ae', '#f1fa3c',
                  '#e28316', '#43658b', '#aa26da', '#fa163f', '#898d90', '#fa26a0', '#05dfd7', '#a3f7bf',
                  '#d68060', '#532e1c', '#59886b', '#db6400']


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
        if children is None:
            children = []
        super().__init__(lst)
        self.name = name
        self.parent = parent
        self.children = children

    def update(self, contents: list):
        self.clear()
        self.extend(contents)

    def set_children(self, children: list):
        self.children = children


class LightningReconstructor:
    def __init__(self, max_branch):
        self.max_branch = max_branch
        self.tree = ListNode('root')
        self.lonely = ListNode('lonely')
        self.counter = 0
        self.labelling = True

    def label(self):
        """
        Method to label all the given data points with their branch. The result is a tree of ListNode's with every node
        representing a branch and containing the indices of the data points which are part of that branch.
        """
        pass

    def get_x(self):
        """
        :return: The list of x-coordinates of the stored source points.
        """
        return []

    def get_y(self):
        """
        :return: The list of y-coordinates of the stored source points.
        """
        return []

    def get_z(self):
        """
        :return: The list of z-coordinates of the stored source points.
        """
        return []

    def get_t(self):
        """
        :return: The list of t-coordinates of the stored source points.
        """
        return []

    def plot_tree(self):
        t_plot = self.get_t()
        x_plot = self.get_x()
        y_plot = self.get_y()
        z_plot = self.get_z()

        fig = plt.figure(1, figsize=(20, 10))

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

        for _, _, node in RenderTree(self.tree.children[0]):
            counter = int(node.name[1:])
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

    def identify_data(self, branch=0):
        t_plot = self.get_t()
        x_plot = self.get_x()
        y_plot = self.get_y()
        z_plot = self.get_z()

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

    def plot_FT(self):
        t_plot = self.get_t()
        x_plot = self.get_x()
        y_plot = self.get_y()
        z_plot = self.get_z()

        fig = plt.figure(2, figsize=(20, 10))

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
            # ft2 = fgrid2[0, :]
            fx2 = fgrid2[1, :]
            fy2 = fgrid2[2, :]
            fz2 = fgrid2[3, :]

            ax2.scatter(abs(fx2), abs(fy2), abs(fz2), color=color, marker='o')
            ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')
            counter += 1

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        plt.show()

    def line_plot(self):
        t_plot = self.get_t()

        nodes_per_level = [tup for tup in LevelGroupOrderIter(self.tree)]
        nodes_per_level = nodes_per_level[1:]
        x_positions = [[0] * len(el) for el in nodes_per_level]

        n = len(nodes_per_level)
        min_displacement = 10 + self.counter * 10

        fig = plt.figure(3, figsize=(10, 5))
        ax = fig.add_subplot(111)
        ax.set_xlabel('Time')

        for level in range(len(nodes_per_level)):
            x_append = []
            x_parents = x_positions[level - 1]
            for node in nodes_per_level[level]:
                begin = t_plot[min(node)]
                # end = t_plot[max(node)]

                if level == 0:
                    x = 0
                    x_append.append(x)
                else:
                    ind = nodes_per_level[level - 1].index(node.parent)
                    x = x_parents[ind] + (-1) ** (node.parent.children.index(node)) * 2 ** (
                                n - level) * min_displacement
                    x_append.append(x)
                    ax.plot([begin, begin], [x_parents[ind], x], linestyle=':', color='black')

                counter = int(node.name[1:])
                color = mcolors.hex2color(LIST_OF_COLORS[int(counter % len(LIST_OF_COLORS))])
                ax.scatter(t_plot[node], [x]*len(node), color=color)
                # ax.text(t_plot[node[0]]-0.001, x, f'{node.name}')
            x_positions[level] = x_append

        ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
        plt.show()

    def give_branch(self, branch):
        t_plot = self.get_t()
        x_plot = self.get_x()
        y_plot = self.get_y()
        z_plot = self.get_z()

        node_indices = self.give_branch_ind(branch)
        x = [x_plot[ind] for ind in node_indices]
        y = [y_plot[ind] for ind in node_indices]
        z = [z_plot[ind] for ind in node_indices]
        t = [t_plot[ind] for ind in node_indices]

        return t, x, y, z

    def give_branch_ind(self, branch):
        node = findall_by_attr(self.tree, 'n' + str(branch))
        return node[0]

    def render_tree(self):
        """
        Render the internal tree
        """
        for pre, _, node in RenderTree(self.tree):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), len(node))

    def save_tree_to_file(self, file):
        f = open('../Pickle_saves/' + file, 'wb')
        pickle.dump(self.tree, f)

    def load_tree_from_file(self, file):
        f = open('../Pickle_saves/' + file, 'rb')
        self.tree = pickle.load(f)
