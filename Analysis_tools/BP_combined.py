import numpy as np
import matplotlib.pyplot as plt
from Lightcone_approach.LightningAnalyzer import Analyzer as LightningAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer


data = np.genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

dataname = 'combined'

bp_altitudes_lightcone = []
bp_altitudes_mesh = []
z_hist = []

dataset = 'subset_1'
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

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

z_hist.extend(zcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_lightcone.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_lightcone.append(branch_z[ind])

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_mesh.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_mesh.append(branch_z[ind])

dataset = 'subset_2'
xmin = x > 3000
xmax = x < 7000
ymin = y > -8000
ymax = y < -6000
zmin = z > 5000
zmax = z < 10000
selection = zmin * zmax * xmin * xmax * ymin * ymax
xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

z_hist.extend(zcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_lightcone.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_lightcone.append(branch_z[ind])

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_mesh.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_mesh.append(branch_z[ind])

dataset = 'subset_3'
xmin = x > -4500
xmax = x < -3000
ymin = y > -8500
ymax = y < -5000
zmin = z > 3000
zmax = z < 5000
selection = zmin * zmax * xmin * xmax * ymin * ymax
xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

z_hist.extend(zcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_lightcone.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_lightcone.append(branch_z[ind])

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_mesh.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_mesh.append(branch_z[ind])

dataset = 'subset_4'
xmin = x > 6000
xmax = x < 10000
ymin = y > -13000
ymax = y < -10000
zmin = z > 0
zmax = z < 4000
tmin = t > 1.15
tmax = t < 1.17
selection = zmin * zmax * xmin * xmax * ymin * ymax * tmin * tmax
xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

z_hist.extend(zcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_lightcone.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_lightcone.append(branch_z[ind])

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, branch_z, leaf = analyzer_mesh.give_branch(i)
    if not leaf:
        ind = np.argmax(t_branch)
        bp_altitudes_mesh.append(branch_z[ind])


fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)
counts1, bins1, _ = ax1.hist(bp_altitudes_lightcone, orientation='horizontal', range=(1750, 6250), bins=20)
ax1.set_xlabel(r'Number of branching points')
ax1.set_ylabel(r'Altitude $(m)$')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)
counts2, bins2, _ = ax2.hist(bp_altitudes_mesh, orientation='horizontal', range=(1750, 6250), bins=20)
ax2.set_xlabel(r'Number of branching points')
ax2.set_ylabel(r'Altitude $(m)$')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/bp_data_' + dataname + '.png')

fig2 = plt.figure(figsize=(16, 8))

z_weight = np.histogram(z_hist, bins=bins1)
ax3 = fig2.add_subplot(121)
ax3.hist(bins1[:-1], bins1, orientation='horizontal', range=(1750, 6250), weights=counts1/z_weight[0])
ax3.set_xlabel(r'Number of branching points normalized to number of events')
ax3.set_ylabel(r'Altitude $(m)$')
ax3.set_title(r'Light cone algorithm')

z_weight = np.histogram(z_hist, bins=bins2)
ax4 = fig2.add_subplot(122)
ax4.hist(bins2[:-1], bins2, orientation='horizontal', range=(1750, 6250), weights=counts2/z_weight[0])
ax4.set_xlabel(r'Number of branching points normalized to number of events')
ax4.set_ylabel(r'Altitude $(m)$')
ax4.set_title(r'Voxel algorithm')

fig2.savefig('Figures/bp_ratio_data_' + dataname + '.png', bbox_inches='tight')
