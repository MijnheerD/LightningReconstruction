"""
#1 : min = 50, max=200
#2 : min = 50, max=300
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

xmin = x > 3000
xmax = x < 7000
ymin = y > -8000
ymax = y < -6000
zmin = z > 5000
zmax = z < 10000
selection = zmin * zmax * ymin * ymax * xmin * xmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=400)
print("Start refinement")
tree.octree.refine(min_side=tree.min_voxel_size, max_side=tree.max_voxel_size)
print("Refinement done")
tree.octree.plot()

# tree.label()
# tree.plot_tree()
