import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from collections import deque


def unit_vector(vector):
    """
    Returns the unit vector of the vector.
    """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """
    Calculate the angle between 2 n-dimensional vectors.
    :param v1: First vector.
    :param v2: Second vector, must have some dimension as the first one.
    :return: The angle between the two in radians.
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


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


class Tracker:
    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, t: np.ndarray,
                 seed, weights=(1, 0), d_cut=1000, direction=-1, max_points=200):
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.pool = deque([seed])
        self.distance_weight, self.vel_weight = weights
        self.distance_cutoff = d_cut
        self.direction = direction
        self.search = True
        self.max_points = max_points

    def reset_to_seed(self, seed):
        self.pool = deque([seed])
        self.search = True

    def in_lightcone(self, p: int):
        """
        Check which points are within the lightcone of the current selected point and returns those that are close
        enough to the selected point.
        :param p: Index in the data of the current selected point.
        :return: List of booleans pointing if points are in the lightcone or not.
        """
        x0, y0, z0, t0 = self.x[p], self.y[p], self.z[p], self.t[p]

        # Use speed of lightning propagation (but account for location error)
        c = 3 * 10 ** 8

        # Calculate spacetime interval
        ds = -c ** 2 * (self.t - t0) ** 2 + (self.x - x0) ** 2 + (self.y - y0) ** 2 + (self.z - z0) ** 2
        selection = ds <= 0

        # Points must be close enough to be eligible
        limit_d = np.sqrt((self.x - x0) ** 2 + (self.y - y0) ** 2 + (self.z - z0) ** 2) <= self.distance_cutoff
        if self.direction == 1:
            limit_t = self.t >= t0
        elif self.direction == -1:
            limit_t = self.t <= t0
        else:
            raise Exception("Unknown direction for search")

        return selection * limit_d * limit_t

    def _distance_pair(self, p1, p2):
        """
        Calculate the Euclidean distance between 2 points.
        :param p1: Index in the data of the first selected point.
        :param p2: Index in the data of the second selected point.
        :return: Euclidean distance.
        """
        x1, y1, z1 = self.x[p1], self.y[p1], self.z[p1]
        x2, y2, z2 = self.x[p2], self.y[p2], self.z[p2]

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

    def _velocity_penalty(self, v1, v2):
        """
        Gives a measure from how much two velocity vectors are aligned.
        :param v1: First velocity vector, tuple or list of 2 indices.
        :param v2: Second velocity vector, same format as first.
        :return: Number between 0 and 1. Close to 0 means that the two vector are aligned, 1 indicates anti-aligned.
        """
        p1, p2 = v1
        vel1 = [self.x[p2] - self.x[p1], self.y[p2] - self.y[p1], self.z[p2] - self.z[p1]]
        p1, p2 = v2
        vel2 = [self.x[p2] - self.x[p1], self.y[p2] - self.y[p1], self.z[p2] - self.z[p1]]
        angle = angle_between(np.array(vel1), np.array(vel2))

        return np.sin(angle / 2)

    def _find_next(self, index, prev):
        indices = np.array(range(len(self.t)))
        values = {}

        # Find all the points inside the light cone of currently selected point
        element = self.pool[index]
        select = self.in_lightcone(element)
        possible_points = indices[select]

        # Check for closest points in Euclidean distance, considering also an alignment penalty
        for point in possible_points:
            if point not in self.pool:
                d = self._distance_pair(element, point)
                v = self._velocity_penalty((self.pool[prev], element), (element, point))
                values[point] = self.distance_weight * d + self.vel_weight * v

        return values

    def find_next(self):
        """
        Finds next points at either begin and tail of the current researched branch.
        :return: Index of last added point or None if nothing can be found
        """
        if self.direction == -1:
            index = 0
            prev = 1

            values = self._find_next(index, prev)

            if len(values) == 0:
                self.search = False
                return

            seed_add = min(values, key=values.__getitem__)
            self.pool.appendleft(seed_add)

        elif self.direction == 1:
            index = -1
            prev = -2

            values = self._find_next(index, prev)

            if len(values) == 0:
                self.search = False
                return

            seed_add = min(values, key=values.__getitem__)
            self.pool.append(seed_add)

        else:
            raise ValueError('Direction not valid')

        return seed_add

    def first_step(self):
        assert len(self.pool) == 1, "This is not the first step"

        seed_x = self.x[self.pool[0]]
        seed_y = self.y[self.pool[0]]
        seed_z = self.z[self.pool[0]]
        max_distance = 200

        neighbours = (self.x - seed_x) ** 2 + (self.y - seed_y) ** 2 + (self.z - seed_z) ** 2 <= max_distance
        indices = np.array(range(len(self.t)))
        indices_neighbours = indices[neighbours]

        # Make sure to include at least 1 neighbouring point
        while len(indices_neighbours) < 2 and max_distance <= self.distance_cutoff:
            max_distance += 100
            neighbours = (self.x - seed_x) ** 2 + (self.y - seed_y) ** 2 + (self.z - seed_z) ** 2 <= max_distance**2
            indices_neighbours = indices[neighbours]

        # Find the distance to each neighbour
        distances = {}
        for index in indices_neighbours:
            if index == self.pool[0]:
                continue
            distances[index] = self._distance_pair(self.pool[0], index)

        # Find the minimum and append to pool
        if len(distances) == 0:
            return self.pool[0]

        start = min(distances, key=distances.__getitem__)
        if self.direction == -1:
            self.pool.appendleft(start)
        elif self.direction == 1:
            self.pool.append(start)

        return start

    def run(self):
        self.first_step()
        while self.search:
            # print(f'Still looping, already selected {len(self.pool) - 1} new points')
            self.find_next()
            if len(self.pool) >= self.max_points:
                break

    def run_graph(self):
        fig = plt.figure(1, figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        plt.ion()
        plt.show()

        cmap = cm.plasma
        norm = col.Normalize(vmin=min(self.t), vmax=max(self.t))
        ax.scatter(self.x, self.y, self.z, marker='^', c=self.t, cmap=cmap, norm=norm, alpha=0.2)
        ax.plot(self.x[self.pool[0]], self.y[self.pool[0]], self.z[self.pool[0]],
                marker='o', c='lime', fillstyle='none')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Selection algorithm')
        fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))

        plt.draw()
        plt.pause(0.001)
        input('Press enter to continue: ')

        self.first_step()

        if self.direction == -1:
            ax.plot(self.x[self.pool[0]], self.y[self.pool[0]], self.z[self.pool[0]],
                    marker='o', c='navy', fillstyle='none')
        elif self.direction == 1:
            ax.plot(self.x[self.pool[-1]], self.y[self.pool[-1]], self.z[self.pool[-1]],
                    marker='o', c='navy', fillstyle='none')

        plt.draw()
        plt.pause(0.001)
        input('Press enter to continue: ')

        while self.search:
            self.find_next()

            if self.direction == -1:
                ax.plot(self.x[self.pool[0]], self.y[self.pool[0]], self.z[self.pool[0]],
                        marker='o', c='navy', fillstyle='none')
            elif self.direction == 1:
                ax.plot(self.x[self.pool[-1]], self.y[self.pool[-1]], self.z[self.pool[-1]],
                        marker='o', c='navy', fillstyle='none')

            print(f'Still looping, already selected {len(self.pool) - 1} new points')

            plt.draw()
            plt.pause(0.001)
            input('Press enter to continue: ')

            if len(self.pool) >= self.max_points:
                break
