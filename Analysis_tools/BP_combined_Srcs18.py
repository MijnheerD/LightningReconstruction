import numpy as np
import matplotlib.pyplot as plt
from Lightcone_approach.LightningAnalyzer import Analyzer as LightningAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer


data = np.genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

dataname = 'combined'

bp_altitudes_lightcone = []
bp_altitudes_mesh = []
z_hist = []

dataset = 'subset_1'
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

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=100)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")

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
'''
dataset = 'subset_2'
xmin = x > 60000
xmax = x < 70000
ymin = y > -50000
ymax = y < -40000
zmin = z > 2000
zmax = z < 5500
tmin = t > 1.14
tmax = t < 1.18
chi2max = chi2 < 16
selection = chi2max * zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax
xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=100)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")

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
xmin = x > 60000
xmax = x < 70000
ymin = y > -50000
ymax = y < -40000
zmin = z > 2000
zmax = z < 5500
tmin = t > 1.0
tmax = t < 1.13
chi2max = chi2 < 16
selection = chi2max * zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax
xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=100)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")

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
'''
dataset = 'subset_4'
xmin = x > 60000
xmax = x < 70000
ymin = y > -50000
ymax = y < -40000
zmin = z > 2000
zmax = z < 5500
tmin = t > 1.22
tmax = t < 1.30
chi2max = chi2 < 16
selection = chi2max * zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax
xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_lightcone = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=100, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")

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

fig.savefig('Figures/bp_srcs18_' + dataname + '.png')

fig2 = plt.figure(figsize=(16, 8))

z_weight = np.histogram(z_hist, bins=bins1)
ax3 = fig2.add_subplot(121)
w = counts1/z_weight[0]
w[np.isnan(w)] = 0
ax3.hist(bins1[:-1], bins1, orientation='horizontal', range=(1750, 6250), weights=w)
ax3.set_xlabel(r'Number of branching points normalized to number of events')
ax3.set_ylabel(r'Altitude $(m)$')
ax3.set_title(r'Light cone algorithm')

z_weight = np.histogram(z_hist, bins=bins2)
ax4 = fig2.add_subplot(122)
w = counts2/z_weight[0]
w[np.isnan(w)] = 0
ax4.hist(bins2[:-1], bins2, orientation='horizontal', range=(1750, 6250), weights=w)
ax4.set_xlabel(r'Number of branching points normalized to number of events')
ax4.set_ylabel(r'Altitude $(m)$')
ax4.set_title(r'Voxel algorithm')

fig2.savefig('Figures/bp_ratio_srcs18_' + dataname + '.png', bbox_inches='tight')
