import pickle
import numpy as np  # Only necessary for FT
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
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
    def __init__(self, max_branch, type='Reconstructor'):
        self.max_branch = max_branch
        self.tree = ListNode('root')
        self.lonely = ListNode('lonely')
        self.counter = 0
        self.labelling = True
        self.type = type

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

    def plot_tree(self, filename=None, lonely=True, text=False):
        t_plot = self.get_t()
        x_plot = self.get_x()
        y_plot = self.get_y()
        z_plot = self.get_z()

        if self.type == 'Lightcone':
            fig = plt.figure(1, figsize=(6, 10))
            algo = 'light cone'
        elif self.type == 'Mesh':
            fig = plt.figure(2, figsize=(6, 10))
            algo = 'voxel'
        else:
            fig = plt.figure(3, figsize=(6, 10))
            algo = ''

        cmap = cm.plasma
        norm = mcolors.Normalize(vmin=t_plot[0], vmax=t_plot[-1])

        ax1 = fig.add_subplot(211, projection='3d')
        ax1.scatter(x_plot, y_plot, z_plot, marker='^', c=t_plot, cmap=cmap, norm=norm)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('Time ordered original data')

        ax2 = fig.add_subplot(212, projection='3d')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title(f'Branches selected by the {algo} algorithm')
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
            if text:
                ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')
        if lonely:
            for _, _, node in RenderTree(self.lonely):
                ax2.scatter([x_plot[ind] for ind in node], [y_plot[ind] for ind in node],
                            [z_plot[ind] for ind in node], color='k', marker='s')
                if node.name == 'lonely':
                    continue
                ax2.text(x_plot[node[0]], y_plot[node[0]], z_plot[node[0]], f'{node.name}')

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax1, location='left', shrink=0.8, pad=0.01)
        if filename is not None:
            fig.savefig('Treeplots/' + self.type + '/' + filename + '.png', bbox_inches='tight')
        else:
            plt.show()

        plt.close(fig)

    def plot_tree_projections(self, filename=None):
        x_plot = self.get_x()
        y_plot = self.get_y()
        z_plot = self.get_z()

        if self.type == 'Lightcone':
            fig = plt.figure(1, figsize=(8, 8))
            fig.suptitle('Branches selected by the light cone algorithm')

        elif self.type == 'Mesh':
            fig = plt.figure(2, figsize=(8, 8))
            fig.suptitle('Branches selected by the voxel algorithm')
        else:
            fig = plt.figure(3, figsize=(8, 8))
            fig.suptitle('Branches selected by the algorithm')

        # Create axes and set the ticks to be inside the axes area
        ax = [fig.add_subplot(2, 2, 1), fig.add_subplot(2, 2, 3), fig.add_subplot(2, 2, 4)]
        for a in ax:
            a.tick_params(axis="y", direction="in", right=True, top=True)
            a.tick_params(axis="x", direction="in", right=True, top=True)

        # Remove space between axes and share the relevant ax
        fig.subplots_adjust(wspace=0, hspace=0)
        ax[0].sharex(ax[1])
        ax[1].sharey(ax[2])

        # Set tick labels false on the shared ax
        plt.setp(ax[0].get_xticklabels(), visible=False)
        plt.setp(ax[2].get_yticklabels(), visible=False)

        # Add grid to central axis for better read ax values on outer axes
        ax[1].grid(linestyle='dotted')

        # Add all the labels
        ax[0].set_ylabel('Height [km]')
        ax[1].set_ylabel('Northing [km]')
        ax[1].set_xlabel('Easting [km]')
        ax[2].set_xlabel('Height [km]')

        for _, _, node in RenderTree(self.tree.children[0]):
            counter = int(node.name[1:])
            color = mcolors.hex2color(LIST_OF_COLORS[int(counter % len(LIST_OF_COLORS))])
            ax[0].scatter([x_plot[ind]/1000 for ind in node], [z_plot[ind]/1000 for ind in node],
                          marker='.', s=5, color=color)
            ax[1].scatter([x_plot[ind]/1000 for ind in node], [y_plot[ind]/1000 for ind in node],
                          marker='.', s=5, color=color)
            ax[2].scatter([z_plot[ind]/1000 for ind in node], [y_plot[ind]/1000 for ind in node],
                          marker='.', s=5, color=color)

        if filename is not None:
            fig.savefig('Projections/' + self.type + '/' + filename + '.png', bbox_inches='tight')
        else:
            plt.show()

        plt.close(fig)

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
            node = findall_by_attr(self.tree, 'n' + str(branch))
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

        fig = plt.figure(10, figsize=(20, 10))

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

    def line_plot(self, filename=None):
        t_plot = self.get_t()

        nodes_per_level = [tup for tup in LevelGroupOrderIter(self.tree)]
        nodes_per_level = nodes_per_level[1:]
        x_positions = [[0] * len(el) for el in nodes_per_level]

        n = len(nodes_per_level)
        min_displacement = 10 + n * 10

        if self.type == 'Lightcone':
            fig = plt.figure(4, figsize=(8, 11))
        elif self.type == 'Mesh':
            fig = plt.figure(5, figsize=(8, 11))
        else:
            fig = plt.figure(6, figsize=(8, 11))
        ax = fig.add_subplot(111)
        ax.set_ylabel(r'Time $(s)$')
        ax.invert_yaxis()

        for level in range(n):
            x_append = []
            x_parents = x_positions[level - 1]
            for node in nodes_per_level[level]:
                begin = t_plot[min(node)]

                if level == 0:
                    x = 0
                    x_append.append(x)
                else:
                    ind = nodes_per_level[level - 1].index(node.parent)
                    x = x_parents[ind] + (-1) ** (node.parent.children.index(node)) * 2 ** (
                            n - level) * min_displacement
                    x_append.append(x)
                    ax.plot([x_parents[ind], x], [begin, begin], linestyle=':', color='black')

                counter = int(node.name[1:])
                color = mcolors.hex2color(LIST_OF_COLORS[int(counter % len(LIST_OF_COLORS))])
                ax.scatter([x] * len(node), t_plot[node], color=color)
                # ax.text(t_plot[node[0]]-0.001, x, f'{node.name}')
            x_positions[level] = x_append

        ax.tick_params(axis='x', which='both', top=False, bottom=False, labelbottom=False)
        if filename is not None:
            fig.savefig('Lineplots/' + self.type + '/' + filename + '.png', bbox_inches='tight')
        else:
            plt.show()

        plt.close(fig)

    def give_branch(self, branch):
        t_plot = self.get_t()
        x_plot = self.get_x()
        y_plot = self.get_y()
        z_plot = self.get_z()

        node_indices, leaf_node = self.give_branch_ind(branch)
        x = [x_plot[ind] for ind in node_indices]
        y = [y_plot[ind] for ind in node_indices]
        z = [z_plot[ind] for ind in node_indices]
        t = [t_plot[ind] for ind in node_indices]

        return t, x, y, z, leaf_node

    def give_branch_ind(self, branch):
        f"""
        Returns the node named n{branch} if every branch is present. After cleaning this is not longer the case and the
        function simply returns the {branch}th branch of the internal tree.
        """
        # node = findall_by_attr(self.tree, 'n' + str(branch))
        node = self.tree.descendants[branch]
        if len(node.children) == 0:
            return node, True
        return node, False

    def nr_of_branches(self):
        return len(self.tree.descendants)

    def render_tree(self):
        """
        Render the internal tree
        """
        for pre, _, node in RenderTree(self.tree):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), len(node))

    def save_tree_to_file(self, file):
        f = open('../Pickle_saves/' + self.type + '/' + file, 'wb')
        pickle.dump(self.tree, f)

    def load_tree_from_file(self, file):
        f = open('./Pickle_saves/' + self.type + '/' + file, 'rb')
        self.tree = pickle.load(f)
