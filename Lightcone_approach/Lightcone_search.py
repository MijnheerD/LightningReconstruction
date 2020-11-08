from Lightcone_approach.LinAlg import angle_between
from sortedcontainers import SortedList
import numpy as np


class Stepper:
    def __init__(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, t: np.ndarray, seed, weights=(1, 0), t_cut=1e-7):
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.pool = SortedList([seed])
        self.distance_weight, self.vel_weight = weights
        self.time_cutoff = t_cut
        self.search = True

    def in_lightcone(self, p: int):
        """
        Check which points are within the lightcone of the current selected point.
        :param p: Index in the data of the current selected point.
        :return: List of booleans pointing if points are in the lightcone or not.
        """
        x0, y0, z0, t0 = self.x[p], self.y[p], self.z[p], self.t[p]

        # Points must be close enough in time to be eligible
        select1 = (t0 - self.time_cutoff) <= self.t
        select2 = self.t <= (t0 + self.time_cutoff)

        # Use speed of lightning propagation
        c = 10 ** 7

        # Calculate spacetime interval
        ds = -c ** 2 * (self.t - t0) ** 2 + (self.x - x0) ** 2 + (self.y - y0) ** 2 + (self.z - z0) ** 2
        selection = ds <= 0

        return selection*select1*select2

    def _distance_pair(self, p1, p2):
        """
        Calculate the Euclidean distance between 2 points.
        :param p1: Index in the data of the first selected point.
        :param p2: Index in the data of the second selected point.
        :return: Euclidean distance.
        """
        x1, y1, z1 = self.x[p1], self.y[p1], self.z[p1]
        x2, y2, z2 = self.x[p2], self.y[p2], self.z[p2]

        return (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2

    def _velocity_penalty(self, v1, v2):
        """
        Gives a measure from how much two velocity vectors are aligned.
        :param v1: First velocity vector, tuple or list of 2 indices.
        :param v2: Second velocity vector, same format as first.
        :return: Number between 0 and 1. Close to 0 means that the two vector are (anti-)aligned.
        """
        p1, p2 = v1
        vel1 = [self.x[p2] - self.x[p1], self.y[p2] - self.y[p1], self.z[p2] - self.z[p1]]
        p1, p2 = v2
        vel2 = [self.x[p2] - self.x[p1], self.y[p2] - self.y[p1], self.z[p2] - self.z[p1]]
        angle = angle_between(vel1, vel2)

        return np.sin(angle)

    def find_next(self):
        """
        Finds next points at both begin and tail of the current researched branch.
        :return:
        """
        for index in [-1, 0]:
            self.search = False
            element = self.pool[index]
            values = {}

            select = self.in_lightcone(element)
            indices = np.array(range(len(self.t)))
            possible_points = set(indices[select])

            for point in possible_points:
                if point not in self.pool:
                    if len(self.pool) == 1:
                        d = self._distance_pair(element, point)
                        v = self._velocity_penalty((element, element), (element, point))
                    else:
                        d = self._distance_pair(element, point)
                        v = self._velocity_penalty((self.pool[int(index + (-1)**index)], element), (element, point))

                    values[point] = self.distance_weight * d + self.vel_weight * v

            if len(values) != 0:
                self.search = True
                seed_add = min(values, key=values.__getitem__)
                self.pool.add(seed_add)

    def run(self):
        while self.search:
            print(f'Still looping, already selected {len(self.pool)} points')
            self.find_next()
