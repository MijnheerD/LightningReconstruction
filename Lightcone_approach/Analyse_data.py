import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.constants import c
from sortedcontainers import SortedList, SortedSet

data = np.genfromtxt("data_test.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]


# Make sure data is sorted by time


def in_spacetime_interval(p):
    x0, y0, z0, t0 = p
    # c = 10**7  # Use speed of lightning propagation
    ds = -c ** 2 * (t - t0) ** 2 + (x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2
    return ds <= 0


def add_weight(p1, p2):
    x1, y1, z1, t1 = p1
    x2, y2, z2, t2 = p2
    w = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
    return w


POINTS = len(t)
POOL = SortedList([np.random.randint(0, POINTS + 1)])  # Start with a random seed
RANGE = np.array(range(POINTS))

update = 1
while update:
    print(f'Still looping, I have already selected {len(POOL)} points')
    update = 0
    points = SortedSet()  # Points reachable from pool of seeds
    comparison = {}

    for el in [POOL[0], POOL[-1]]:
        selection = in_spacetime_interval((x[el], y[el], z[el], t[el]))
        in_cone = RANGE[selection]

        if len(in_cone) != 0:
            update = 1

        for point in in_cone:
            if point not in POOL:
                weight = add_weight((x[el], y[el], z[el], t[el]), (x[point], y[point], z[point], t[point]))
                if point in comparison:
                    old = comparison[point]
                else:
                    old = 1e8

                if weight < old:
                    comparison[point] = weight

    seed_add = min(comparison, key=comparison.__getitem__)
    POOL.add(seed_add)

SELECTION = np.array(POOL)

fig = plt.figure(1, figsize=(20, 10))
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

ax.scatter(x, y, z, marker='^', c='b')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Original data')

ax2.scatter(x[SELECTION], y[SELECTION], z[SELECTION], marker='o', c='r')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Data selected by lightcone algorithm')

fig2 = plt.figure(2, figsize=(15, 15))
ax3 = fig2.add_subplot(111, projection='3d')

ax3.scatter(x, y, z, marker='^', c='b')
ax3.scatter(x[SELECTION], y[SELECTION], z[SELECTION], marker='o', c='r')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
ax3.set_title('Overlap of the selection with the original data')

plt.show()
