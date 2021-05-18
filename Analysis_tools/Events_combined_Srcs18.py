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

events_lightcone = []
bp_lightcone = []
events_mesh = []
bp_mesh = []

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

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    if i > 0:
        bp_lightcone.append(min(t_branch))
    events_lightcone.extend(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    if i > 0:
        bp_mesh.append(min(t_branch))
    events_mesh.extend(t_branch)
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

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    if i > 0:
        bp_lightcone.append(min(t_branch))
    events_lightcone.extend(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    if i > 0:
        bp_mesh.append(min(t_branch))
    events_mesh.extend(t_branch)

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

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    if i > 0:
        bp_lightcone.append(min(t_branch))
    events_lightcone.extend(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    if i > 0:
        bp_mesh.append(min(t_branch))
    events_mesh.extend(t_branch)
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

for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    if i > 0:
        bp_lightcone.append(min(t_branch))
    events_lightcone.extend(t_branch)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    if i > 0:
        bp_mesh.append(min(t_branch))
    events_mesh.extend(t_branch)


fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(211)

ax1.hist(events_lightcone, align='left', bins=50)
ax1.vlines(bp_lightcone, 0, ax1.get_ylim()[1], color="tab:red")

# ax1.set_xlabel(r'Time $(s)$')
ax1.set_ylabel(r'Number of events')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(212)

ax2.hist(events_mesh, align='left', bins=50)
ax2.vlines(bp_mesh, 0, ax2.get_ylim()[1], color="tab:red")

ax2.set_xlabel(r'Time $(s)$')
ax2.set_ylabel(r'Number of events')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/events_srcs18_' + dataname + '.png', bbox_inches='tight')
