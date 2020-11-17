"""
TODO: optimize weights
"""

from Lightcone_approach.LinAlg import angle_between
from collections import deque
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Stepper:
    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, t: np.ndarray, seed, weights=(1, 0), d_cut=1000):
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.pool = deque([seed])
        self.distance_weight, self.vel_weight = weights
        self.distance_cutoff = d_cut
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
        limit1 = np.sqrt((self.x - x0) ** 2 + (self.y - y0) ** 2 + (self.z - z0) ** 2) <= self.distance_cutoff

        return selection*limit1

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
        angle = angle_between(vel1, vel2)

        return np.sin(angle / 2)

    def find_next(self):
        """
        Finds next points at both begin and tail of the current researched branch.
        :return:
        """
        self.search = False
        for index, prev in zip([-1, 0], [-2, 1]):
            element = self.pool[index]
            values = {}

            select = self.in_lightcone(element)
            indices = np.array(range(len(self.t)))
            possible_points = indices[select]

            for point in possible_points:
                if point not in self.pool:
                    d = self._distance_pair(element, point)
                    v = self._velocity_penalty((self.pool[prev], element), (element, point))
                    values[point] = self.distance_weight * d + self.vel_weight * v

            if len(values) != 0:
                self.search = True
                seed_add = min(values, key=values.__getitem__)
                if index == -1:
                    self.pool.append(seed_add)
                else:
                    self.pool.appendleft(seed_add)

    def first_step(self):
        assert len(self.pool) == 1, "This is not the first step"

        seed_x = self.x[self.pool[0]]
        seed_y = self.y[self.pool[0]]
        seed_z = self.z[self.pool[0]]
        max_distance = 500

        neighbours = (self.x - seed_x) ** 2 + (self.y - seed_y) ** 2 + (self.z - seed_z) ** 2 <= max_distance
        indices = np.array(range(len(self.t)))
        indices_neighbours = indices[neighbours]

        # Make sure to include at least 5 neighbouring points
        while len(indices_neighbours) <= 4:
            max_distance += 100
            neighbours = (self.x - seed_x) ** 2 + (self.y - seed_y) ** 2 + (self.z - seed_z) ** 2 <= max_distance
            indices_neighbours = indices[neighbours]

        # Find the distance to each neighbour
        distances = {}
        for index in indices_neighbours:
            if index == self.pool[0]:
                continue
            distances[index] = self._distance_pair(self.pool[0], index)

        # Try to find the 2 closest neighbours which are almost anti-aligned
        values = {}
        for (index1, index2) in combinations(distances.keys(), 2):
            total_dist = distances[index1] + distances[index2]
            vel_comp = self._velocity_penalty((self.pool[0], index1), (self.pool[0], index2))
            values[(index1, index2)] = total_dist / vel_comp

        # Find the minimum and append to pool
        (start_left, start_right) = min(values, key=values.__getitem__)
        self.pool.appendleft(start_left)
        self.pool.append(start_right)

    def run(self):
        self.first_step()
        while self.search:
            print(f'Still looping, already selected {len(self.pool)} points')
            self.find_next()
            if len(self.pool)>=20:
                break

    def run_graph(self):
        fig = plt.figure(1, figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        plt.ion()
        plt.show()

        ax.scatter(self.x, self.y, self.z, marker='^', c='navy', alpha=0.2)
        ax.scatter(self.x[self.pool[0]], self.y[self.pool[0]], self.z[self.pool[0]], marker='o', c='k')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Selection algorithm')

        plt.draw()
        plt.pause(0.001)
        input('Press enter to continue: ')

        self.first_step()

        ax.scatter(self.x[self.pool[0]], self.y[self.pool[0]], self.z[self.pool[0]], marker='o', c='maroon')
        ax.scatter(self.x[self.pool[-1]], self.y[self.pool[-1]], self.z[self.pool[-1]], marker='o', c='maroon')

        plt.draw()
        plt.pause(0.001)
        input('Press enter to continue: ')

        while self.search:
            self.find_next()

            ax.scatter(self.x[self.pool[0]], self.y[self.pool[0]], self.z[self.pool[0]], marker='o', c='maroon')
            ax.scatter(self.x[self.pool[-1]], self.y[self.pool[-1]], self.z[self.pool[-1]], marker='o', c='maroon')

            print(f'Still looping, already selected {len(self.pool)} points')

            plt.draw()
            plt.pause(0.001)
            input('Press enter to continue: ')

            if len(self.pool) >= 20:
                break