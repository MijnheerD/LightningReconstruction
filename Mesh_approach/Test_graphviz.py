from numpy import genfromtxt
from Mesh_approach.LightningAnalyzer import Analyzer


data = genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

dataname = 'subset_3'
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

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
tree.octree.refine(min_side=tree.min_voxel_size, max_side=tree.max_voxel_size)
tree.octree.make_voxel_graph(dataname+'_unflatten')
