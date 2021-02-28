from numpy import genfromtxt
from Mesh_approach.Mesh_octree import Octree

data = genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > -4500
xmax = x < -3000
ymin = y > -8500
ymax = y < -5000
zmin = z > 3000
zmax = z < 5000
selection = zmin * zmax * ymin * ymax * xmin * xmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

tree = Octree(tcut, xcut, ycut, zcut)
tree.refine()
tree.plot()
