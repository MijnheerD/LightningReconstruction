from numpy import genfromtxt
from Mesh_approach.LightningAnalyzer import Analyzer

data = genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

dataname = 'subset_2'
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

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
tree.octree.refine(min_side=tree.min_voxel_size, max_side=tree.max_voxel_size)
tree.octree.make_voxel_graph(dataname)

'''
graph = Graph(comment='The voxel structure', filename='Graph_subset1', format='png')
voxels = tree.octree.find_leaves(tree.octree.root)
max_score = 700
colormap = cm.get_cmap("inferno")

for counter in range(len(voxels)):
    # Make a node for every voxel, with the size depending on the number of data points inside it
    size = len(voxels[counter].contents)
    graph.node('voxel'+str(counter), label=None, shape='point', fixedsize='true', width=str(0.05*size))

for counter in range(len(voxels)):
    # Draw for every node the edges corresponding to the neighbours
    connection = False
    nn = voxels[counter].neighbours

    # Limit the number of drawn neighbours
    if len(nn) > 3:
        top_nn = dict(sorted(nn.items(), key=lambda k: k[1][1])[:3])
    else:
        top_nn = nn

    # Change the drawing style and color depending on the type and score respectively
    for neighbour in top_nn:
        try:
            pointer = voxels.index(neighbour)
            ninfo = top_nn[neighbour]
            if ninfo[0] == 'face':
                linestyle = 'solid'
            elif ninfo[0] == 'edge':
                linestyle = 'dashed'
            else:
                linestyle = 'dotted'

            if ninfo[1] > max_score:
                print(f"Max score has been exceeded with {ninfo[1]}")
                score = max_score
            else:
                score = ninfo[1]
            norm = score / max_score
            color = rgb_to_hsv(colormap(norm)[0:3])
            graph.edge('voxel' + str(counter), 'voxel' + str(pointer), style=linestyle,
                       color=f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f}")
            connection = True
        except ValueError:
            pass

    # Print out if a lonely voxel has been detected
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
'''
