from numpy import genfromtxt
from graphviz import Graph
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from Mesh_approach.LightningAnalyzer import Analyzer


data = genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

dataname = 'subset_1'
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

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
tree.octree.refine(min_side=tree.min_voxel_size, max_side=tree.max_voxel_size)
tree.octree.make_voxel_graph(dataname+'_unflatten')

'''
voxels = tree.octree.find_leaves(tree.octree.root)
connections = lil_matrix((len(voxels), len(voxels)), dtype='f')  # use float32 to use less memory
for counter in range(len(voxels)):
    nn = voxels[counter].neighbours
    for neighbour in nn:
        pointer = voxels.index(neighbour)
        ninfo = nn[neighbour]
        connections[counter, pointer] = ninfo[1].astype('f')

mst = minimum_spanning_tree(connections)

graph = Graph(comment='Minimum spanning tree', filename='MST_'+dataname, format='png')
for counter in range(len(voxels)):
    # Make a node for every voxel, with the size depending on the number of data points inside it
    size = len(voxels[counter].contents)
    graph.node('voxel' + str(counter), label=None, shape='point', fixedsize='true', width=str(0.05 * size))
    for neighbour in voxels[counter].neighbours:
        pointer = voxels.index(neighbour)
        if mst[counter, pointer]:
            graph.edge('voxel' + str(counter), 'voxel' + str(pointer))

u = graph.unflatten(stagger=3)
u.render()
'''