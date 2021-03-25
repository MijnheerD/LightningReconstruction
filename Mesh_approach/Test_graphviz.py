from numpy import genfromtxt
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

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=20, max_voxel_size=200)
tree.octree.refine(min_side=tree.min_voxel_size, max_side=tree.max_voxel_size)

graph = Graph(comment='The voxel structure', filename='Graph_subset1', format='png')
voxels = tree.octree.find_leaves(tree.octree.root)

for counter in range(len(voxels)):
    if voxels[counter].label != 0:
        graph.node('voxel'+str(counter), label=None, shape='circle')
for counter in range(len(voxels)):
    connection = False
    for neighbour in voxels[counter].neighbours:
        try:
            pointer = voxels.index(neighbour)
            graph.edge('voxel' + str(counter), 'voxel' + str(pointer))
            connection = True
        except ValueError:
            pass
    if not connection:
        print(f"The {counter} voxel at {voxels[counter].center} with edge {voxels[counter].edge} has no connections")
        print(f"This voxel has {len(voxels[counter].neighbours)} neighbours and contains "
              f"{len(voxels[counter].contents)} data points")
        print(f"Its status is {voxels[counter].active}")
        for neighbour in voxels[counter].neighbours:
            if len(neighbour.children) > 0:
                print(f"The neighbour at {neighbour.center} with edge {neighbour.edge} has children")

graph.render()
tree.octree.plot()
