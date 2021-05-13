from numpy import genfromtxt
from anytree import RenderTree
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer

data = genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

dataname = 'Srcs18_subset_1'
xmin = x > 42000
xmax = x < 44000
ymin = y > -17000
ymax = y < -14000
zmin = z > 6000
zmax = z < 8000
tmin = t > 0.95
tmax = t < 1.2
chi2max = chi2 < 16
selection = chi2max * zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=100)
# analyzer_mesh.label()
analyzer_mesh.load_tree_from_file(dataname+".pickle")
analyzer_mesh.render_tree()
analyzer_mesh.plot_tree()

tree = analyzer_mesh.tree
for _, _, node in RenderTree(tree.children[0]):
    if len(node.children) == 0 and len(node) < 20:
        leaf_children = 0
        for child in node.parent.children:
            if len(child.children) == 0:
                pass
        if leaf_children < 2:
            node.parent.extend(node)
            node.parent = None

analyzer_mesh.render_tree()

to_remove = []
for _, _, node in RenderTree(tree.children[0]):
    if len(node.children) == 1:
        node.children[0].extend(node)
        to_remove.append(node)

for node in to_remove:
    node.children[0].parent = node.parent
    node.parent = None

analyzer_mesh.render_tree()
analyzer_mesh.plot_tree(lonely=False)
