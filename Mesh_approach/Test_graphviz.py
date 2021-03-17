from numpy import genfromtxt, log
from graphviz import Graph
from Mesh_approach.LightningAnalyzer import Analyzer

data = genfromtxt("../Data/data.txt", delimiter=",")
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
selection = zmin * zmax * ymin * ymax * xmin * xmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=500, max_voxel_size=1000)
tree.octree.refine(min_side=tree.min_voxel_size, max_side=tree.max_voxel_size)

graph = Graph(comment='The voxel structure', filename='Graph_subset1', format='png')
voxels = tree.octree.find_leaves(tree.octree.root)

for counter in range(len(voxels)):
    if voxels[counter].label != 0:
        graph.node('voxel'+str(counter), label=None, shape='point')
for counter in range(len(voxels)):
    for neighbour in voxels[counter].neighbours:
        try:
            pointer = voxels.index(neighbour)
            graph.edge('voxel' + str(counter), 'voxel' + str(pointer))
        except ValueError:
            pass

graph.render()
tree.octree.plot()
