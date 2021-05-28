import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from Lightcone_approach.LightningAnalyzer import Analyzer as LightningAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer


data = np.genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

dataname = 'combined'

events_lightcone = []
bp_lightcone = []
events_mesh = []
bp_mesh = []

total_lightcone = 0
total_mesh = 0
total = 0

p = 5

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

total += len(tcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_lightcone.append(t_0)
    events_lightcone.extend(t_branch - t_0)
    total_lightcone += len(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_mesh.append(t_0)
    events_mesh.extend(t_branch - t_0)
    total_mesh += len(t_branch)
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

total += len(tcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_lightcone.append(t_0)
    events_lightcone.extend(t_branch - t_0)
    total_lightcone += len(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_mesh.append(t_0)
    events_mesh.extend(t_branch - t_0)
    total_mesh += len(t_branch)

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

total += len(tcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_lightcone.append(t_0)
    events_lightcone.extend(t_branch - t_0)
    total_lightcone += len(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_mesh.append(t_0)
    events_mesh.extend(t_branch - t_0)
    total_mesh += len(t_branch)
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

total += len(tcut)

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_lightcone.append(t_0)
    events_lightcone.extend(t_branch - t_0)
    total_lightcone += len(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    t_0 = np.percentile(t_branch, p)
    bp_mesh.append(t_0)
    events_mesh.extend(t_branch - t_0)
    total_mesh += len(t_branch)


print(f"Light cone has a total of {total_lightcone} number of events")
print(f"Voxel has a total of {total_mesh} number of events")
print(f"The data set has {total} numbers of events")

fig = plt.figure(figsize=(16, 8))
gs = GridSpec(1, 2, figure=fig)

ax1 = fig.add_subplot(gs[0, 0])

ax1.hist(events_lightcone, align='mid', bins=50)
ax1.set_xlim((-0.05, 0.15))
ax1.set_ylim((0, 1600))
ax1.set_xlabel(r'$t - t_0 (s)$')
ax1.set_ylabel(r'Density')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(gs[0, 1:])

ax2.hist(events_mesh, align='mid', bins=50)
ax2.set_xlim((-0.05, 0.15))
ax2.set_ylim((0, 1600))
ax2.set_xlabel(r'$t - t_0 (s)$')
ax2.set_ylabel(r'Density')
ax2.set_title(r'Voxel algorithm')

fig.savefig(f'Figures/ef_srcs18_per{p}_{dataname}.png', bbox_inches='tight')