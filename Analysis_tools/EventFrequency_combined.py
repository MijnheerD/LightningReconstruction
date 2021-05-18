import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from Lightcone_approach.LightningAnalyzer import Analyzer as LightconeAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer


data = np.genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

dataname = 'combined'

events_lightcone = []
bp_lightcone = []
events_mesh = []
bp_mesh = []

total_lightcone = 0
total_mesh = 0
total = 0

p = 1

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_"+dataset+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")

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
ax1.set_xlim((-0.05, 0.3))
ax1.set_ylim((0, 1600))
ax1.set_xlabel(r'$t - t_0 (s)$')
ax1.set_ylabel(r'Density')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(gs[0, 1:])

ax2.hist(events_mesh, align='mid', bins=50)
ax2.set_xlim((-0.05, 0.3))
ax2.set_ylim((0, 1600))
ax2.set_xlabel(r'$t - t_0 (s)$')
ax2.set_ylabel(r'Density')
ax2.set_title(r'Voxel algorithm')
# ax2.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

fig.savefig(f'Figures/ef_data_per{p}_{dataname}.png', bbox_inches='tight')
