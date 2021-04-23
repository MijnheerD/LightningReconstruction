"""
#1 : min = 50, max=200
#2
#3 : min = 50, max>=200
#4 : min = 50, max=100/200
"""

from numpy import genfromtxt
from Mesh_approach.LightningAnalyzer import Analyzer

data = genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > 6000
xmax = x < 10000
ymin = y > -13000
ymax = y < -10000
zmin = z > 0
zmax = z < 4000
tmin = t > 1.15
tmax = t < 1.17
selection = zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=100)
print("Start refinement")
tree.octree.refine(min_side=tree.min_voxel_size, max_side=tree.max_voxel_size)
print("Refinement done")
tree.octree.plot()

# tree.label()
# tree.plot_tree()
