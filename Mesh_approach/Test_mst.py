from numpy import genfromtxt, concatenate, zeros
from scipy.sparse import lil_matrix, diags
from scipy.sparse.csgraph import minimum_spanning_tree
from Mesh_approach.LightningAnalyzer import Analyzer
from graphviz import Graph


def dfs(sym_graph, current_vertex, visited=None):
    # visited is supposed to start at [counter]
    if visited is None:
        visited = []

    # current vertex is index in final_voxels list
    visited.append(current_vertex)
    # we want at least 3 other visited voxels, apart from counter
    if len(visited) > 3:
        return visited

    # assumes graph is in scipy.sparse form and symmetric!
    for neighbour_index in sym_graph[current_vertex].nonzero()[1]:
        if neighbour_index not in visited:
            visited = dfs(sym_graph, neighbour_index, visited)
            if len(visited) > 3:
                return visited

    return visited


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
# tree.octree.make_voxel_graph(dataname)

voxels = tree.octree.find_leaves(tree.octree.root)
connections = lil_matrix((len(voxels), len(voxels)), dtype='f')  # use float32 to use less memory
for counter in range(len(voxels)):
    nn = voxels[counter].neighbours
    for neighbour in nn:
        pointer = voxels.index(neighbour)
        ninfo = nn[neighbour]
        connections[counter, pointer] = ninfo[1].astype('f')

mst = minimum_spanning_tree(connections)
sym = mst + mst.T - diags(mst.diagonal(), dtype='f')  # make mst diagonal

connections = zeros((len(voxels), 3))
BP = []
removed = []
normal_to_absorb = []
for counter in range(len(voxels)):
    for neighbour in sym[counter].nonzero()[1]:
        number_of_connections = len(dfs(sym, neighbour, visited=[counter])) - 1
        if number_of_connections == 1:
            # trivial connection
            connections[counter][0] += 1
            # Absorb the data points of neighbour into the current voxels
            voxels[counter].contents = concatenate([voxels[counter].contents, voxels[neighbour].contents])
            removed.append(neighbour)
            # sym[counter, neighbour] = 0
            # sym[neighbour, counter] = 0
        elif number_of_connections == 2:
            # normal connection
            connections[counter][1] += 1
            normal_to_absorb.append(neighbour)
        else:
            # heavy connection
            connections[counter][2] += 1

    if connections[counter][2] >= 3:
        BP.append(counter)

    if connections[counter][2] >= 2:
        if connections[counter][1] > 0:
            for neighbour in normal_to_absorb:
                voxels[counter].contents = concatenate([voxels[counter].contents, voxels[neighbour].contents])
                removed.append(neighbour)
                # sym[counter, neighbour] = 0
                # sym[neighbour, counter] = 0

    normal_to_absorb = []

graph = Graph(comment='Minimum spanning tree', filename='MST_'+dataname, format='png')
for counter in range(len(voxels)):
    if counter not in removed:
        # Make a node for every voxel, with the size depending on the number of data points inside it
        size = len(voxels[counter].contents)
        if counter in BP:
            color = 'red'
        else:
            color = 'black'
        graph.node('voxel' + str(counter), label=None, shape='point', fixedsize='true',
                   width=str(0.05 * size), color=color)
        for neighbour in voxels[counter].neighbours:
            pointer = voxels.index(neighbour)
            if pointer not in removed:
                if sym[counter, pointer]:
                    graph.edge('voxel' + str(counter), 'voxel' + str(pointer))

graph.render()
