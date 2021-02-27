from numpy import genfromtxt
from Mesh_approach.Mesh_octree import Octree

data = genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > 6000
xmax = x < 10000
ymin = y > -7000
ymax = y < -6000
zmin = z > 0
zmax = z < 3000
tmin = t > 0.85
tmax = t < 1
selection = zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

tree = Octree(tcut, xcut, ycut, zcut)
tree.refine()
tree.plot()
