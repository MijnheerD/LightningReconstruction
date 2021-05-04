"""
Make a histogram of the time lengths of every branch in the flash
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

lengths_lightcone = []
for i in range(analyzer_lightcone.nr_of_branches()):
    branch_t, _, _, _ = analyzer_lightcone.give_branch(i)
    lengths_lightcone.append(max(branch_t) - min(branch_t))

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataname + ".pickle")

lengths_mesh = []
for i in range(analyzer_mesh.nr_of_branches()):
    branch_t, _, _, _ = analyzer_mesh.give_branch(i)
    lengths_mesh.append(max(branch_t) - min(branch_t))

fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)
ax1.hist(lengths_lightcone, align='left')
ax1.set_xlabel(r'Time length of branches $(s)$')
ax1.set_ylabel(r'Density')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)
ax2.hist(lengths_mesh, align='left')
ax2.set_xlabel(r'Time length of branches $(s)$')
ax2.set_ylabel(r'Density')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/timelength_data_' + dataname + '.png')
