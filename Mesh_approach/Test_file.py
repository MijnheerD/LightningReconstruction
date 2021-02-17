import numpy as np
from Mesh_approach.Mesh_fixed_res import Space, ijk2n

data = np.genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > 6000
xmax = x < 9000
ymin = y > -6000
ymax = y < -3000
zmin = z > 1500
zmax = z < 5000
selection = zmin * zmax * xmin * xmax * ymin * ymax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

space = Space(tcut, xcut, ycut, zcut, 100)
space.plot_split()

data = space.split()
number = int(space.side / space.res)
max_n = ijk2n(number-1, number-1, number-1, number)
not_yet = []
for k in range(number):
    for j in range(number):
        for i in range(number):
            n = ijk2n(i, j, k, number)
            neighbours = [ijk2n(i - 1, j - 1, k - 1, number), ijk2n(i - 1, j, k - 1, number),
                          ijk2n(i - 1, j + 1, k - 1, number),
                          ijk2n(i, j - 1, k - 1, number), ijk2n(i, j, k - 1, number),
                          ijk2n(i, j + 1, k - 1, number),
                          ijk2n(i + 1, j - 1, k - 1, number), ijk2n(i + 1, j, k - 1, number),
                          ijk2n(i + 1, j + 1, k - 1, number),

                          ijk2n(i - 1, j - 1, k, number), ijk2n(i - 1, j, k, number),
                          ijk2n(i - 1, j + 1, k, number),
                          ijk2n(i, j - 1, k, number), ijk2n(i, j + 1, k, number),
                          ijk2n(i + 1, j - 1, k, number), ijk2n(i + 1, j, k, number),
                          ijk2n(i + 1, j + 1, k, number),

                          ijk2n(i - 1, j - 1, k + 1, number), ijk2n(i - 1, j, k + 1, number),
                          ijk2n(i - 1, j + 1, k + 1, number),
                          ijk2n(i, j - 1, k + 1, number), ijk2n(i, j, k + 1, number),
                          ijk2n(i, j + 1, k + 1, number),
                          ijk2n(i + 1, j - 1, k + 1, number), ijk2n(i + 1, j, k + 1, number),
                          ijk2n(i + 1, j + 1, k + 1, number),
                          ]
            if len(data[n]) != 0:
                count = 0
                for neigh in neighbours:
                    if neigh < 0 or neigh > max_n:
                        pass
                    else:
                        if len(data[neigh]) != 0:
                            count += 1
                if count > 3:
                    not_yet.append(n)


print(not_yet)
