import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm


def ijk2n(i, j, k, number):
    return i + j * number + k * number ** 2


def n2ijk(n, number):
    k = np.floor(n / number ** 2)
    j = np.floor((n - k * number ** 2) / number)
    i = n - j * number - k * number ** 2
    return int(i), int(j), int(k)


class Space:
    def __init__(self, t, x, y, z, res):
        txyz = sorted(zip(t, x, y, z))
        self.t, self.x, self.y, self.z = map(np.array, zip(*list(txyz)))
        self.centre = np.array([(x.min() + x.max()) / 2, (y.min() + y.max()) / 2, (z.min() + z.max()) / 2])
        self.res = res

        longest_side = np.max([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()])
        self.side = res * np.ceil(longest_side / res)

    def _split_self(self):
        number = int(self.side / self.res)
        begin = self.centre - self.side / 2

        x = [begin[0] + self.res * i for i in range(number + 1)]
        y = [begin[1] + self.res * i for i in range(number + 1)]
        z = [begin[2] + self.res * i for i in range(number + 1)]

        return np.array(x), np.array(y), np.array(z)

    def _split_x(self, x_list):
        result = []
        for i in range(len(x_list) - 1):
            min = self.x > x_list[i]
            max = self.x < x_list[i+1]
            result.append(np.where(min * max)[0].tolist())
        return result

    def _split_y(self, y_list, selection):
        y_considered = [self.y[idx] for idx in selection]
        result = []
        for i in range(len(y_list) - 1):
            min = y_considered > y_list[i]
            max = y_considered < y_list[i + 1]
            temp = np.where(min * max)[0]
            result.append([selection[idx] for idx in temp])
        return result

    def _split_z(self, z_list, selection):
        z_considered = [self.z[idx] for idx in selection]
        result = []
        for i in range(len(z_list) - 1):
            min = z_considered > z_list[i]
            max = z_considered < z_list[i + 1]
            temp = np.where(min * max)[0]
            result.append([selection[idx] for idx in temp])
        return result

    def split(self):
        n = int(self.side / self.res)
        x, y, z = self._split_self()

        points_in_block_n =[0]*ijk2n(n-1, n-1, n-1, n)
        i, j, k = 0, 0, 0
        x_divided = self._split_x(x)
        for col in x_divided:
            y_divided = self._split_y(y, col)
            for row in y_divided:
                z_divided = self._split_z(z, row)
                for line in z_divided:
                    points_in_block_n[ijk2n(i, j, k, n)-1] = line
                    k += 1
                j+= 1
                k = 0
            i+=1
            j = 0
            k = 0

        return points_in_block_n

    def plot_split(self):
        data = self.split()
        x, y, z = self._split_self()
        number = int(self.side / self.res)

        fig = plt.figure(1, figsize=(20, 10))
        ax1 = fig.add_subplot(121, projection='3d')
        ax2 = fig.add_subplot(122, projection='3d')

        cmap = cm.plasma
        norm = mcolors.Normalize(vmin=self.t[0], vmax=self.t[-1])

        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('Time ordered original data')
        ax1.scatter(self.x, self.y, self.z, marker='^', c=self.t, cmap=cmap, norm=norm)

        cmap2 = cm.summer
        norm2 = mcolors.Normalize(vmin=0, vmax=len(self.t)/number)

        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('Total number of filled voxels')
        (left, right) = ax1.get_xlim3d()
        ax2.set_xlim3d(left, right)
        (left, right) = ax1.get_ylim3d()
        ax2.set_ylim3d(left, right)
        (left, right) = ax1.get_zlim3d()
        ax2.set_zlim3d(left, right)
        ax2.scatter(self.x, self.y, self.z, marker='x', c=self.t, cmap=cmap, norm=norm)

        for n in range(len(data)):
            set = data[n]
            if len(set) == 0:
                pass
            else:
                i, j, k = n2ijk(n+1, number)
                x_plot = (x[i] + x[i+1]) / 2
                y_plot = (y[j] + y[j+1]) / 2
                z_plot = (z[k] + z[k+1]) / 2
                ax2.scatter(x_plot, y_plot, z_plot, c=len(set), cmap=cmap2, norm=norm2)

        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax1)
        fig.colorbar(cm.ScalarMappable(norm=norm2, cmap=cmap2), ax=ax2)
        plt.show()
