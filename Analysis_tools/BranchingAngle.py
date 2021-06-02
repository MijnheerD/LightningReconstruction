"""
Make a histogram of the angle between two splitting branches
"""

import numpy as np
import matplotlib.pyplot as plt
from Lightcone_approach.LightningAnalyzer import Analyzer as LightconeAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer

data = np.genfromtxt("../Data/data.txt", delimiter=",")
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
selection = zmin * zmax * xmin * xmax * ymin * ymax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

angles_lightcone = []
angles_mesh = []

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_" + dataname + ".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataname + ".pickle")

x_plot = np.array(analyzer_lightcone.get_x())
y_plot = np.array(analyzer_lightcone.get_y())
z_plot = np.array(analyzer_lightcone.get_z())

node, leaf = analyzer_lightcone.give_branch_ind(0)
indices_0 = sorted(node.children[0])[:10]
indices_1 = sorted(node.children[1])[:10]
data_0 = np.concatenate((x_plot[indices_0, np.newaxis],
                         y_plot[indices_0, np.newaxis],
                         z_plot[indices_0, np.newaxis]),
                        axis=1)
data_1 = np.concatenate((x_plot[indices_1, np.newaxis],
                         y_plot[indices_1, np.newaxis],
                         z_plot[indices_1, np.newaxis]),
                        axis=1)
# Calculate the mean of the points, i.e. the 'center' of the cloud
datamean_0 = data_0.mean(axis=0)
datamean_1 = data_1.mean(axis=0)

# Do an SVD on the mean-centered data.
_, _, vv_0 = np.linalg.svd(data_0 - datamean_0)
_, _, vv_1 = np.linalg.svd(data_1 - datamean_1)

linepts_0 = vv_0[0] * np.mgrid[-1000:1000:2j][:, np.newaxis]
linepts_1 = vv_1[0] * np.mgrid[-1000:1000:2j][:, np.newaxis]

linepts_0 += datamean_0
linepts_1 += datamean_1

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x_plot[node], y_plot[node], z_plot[node])
ax.scatter(x_plot[indices_0], y_plot[indices_0], z_plot[indices_0], c='orange')
ax.scatter(x_plot[indices_1], y_plot[indices_1], z_plot[indices_1], c='green')

ax.plot(*linepts_0.T, c='orange')
ax.plot(*linepts_1.T, c='green')

plt.show()
