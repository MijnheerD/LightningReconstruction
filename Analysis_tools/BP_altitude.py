"""
Make a histogram of the number of branches points vs altitude
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

bp_altitudes_lightcone = []
for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_lightcone.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_lightcone.append(branch_z[ind])

bp_altitudes_mesh = []
for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_mesh.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_mesh.append(branch_z[ind])

fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)
ax1.hist(bp_altitudes_lightcone, orientation='horizontal', align='left')
ax1.set_xlabel(r'Density')
ax1.set_ylabel(r'Altitude $(m)$')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)
ax2.hist(bp_altitudes_mesh, orientation='horizontal', align='left')
ax2.set_xlabel(r'Density')
ax2.set_ylabel(r'Altitude $(m)$')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/bp_data_' + dataname + '.png')
