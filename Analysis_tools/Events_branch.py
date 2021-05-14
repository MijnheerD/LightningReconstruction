"""
Make a histogram of the number of events along a branch and plot it against the location of BP in time
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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataname+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataname + ".pickle")

events_lightcone = []
bp_lightcone = []
for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    if i > 0:
        bp_lightcone.append(min(t_branch))
    events_lightcone.extend(t_branch)

events_mesh = []
bp_mesh = []
for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    if i > 0:
        bp_mesh.append(min(t_branch))
    events_mesh.extend(t_branch)

fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)

ax1.hist(events_lightcone, align='left', bins=50)
ax1.vlines(bp_lightcone, 0, ax1.get_ylim()[1], color="tab:red")

ax1.set_xlabel(r'Time $(s)$')
ax1.set_ylabel(r'Density')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)

ax2.hist(events_mesh, align='left', bins=50)
ax2.vlines(bp_mesh, 0, ax2.get_ylim()[1], color="tab:red")

ax2.set_xlabel(r'Time $(s)$')
ax2.set_ylabel(r'Density')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/events_data_' + dataname + '.png')
