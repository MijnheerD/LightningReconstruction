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

lengths_lightcone = []
lengths_mesh = []

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

for i in range(analyzer_lightcone.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_lightcone.give_branch(i)
    lengths_lightcone.append(max(branch_t) - min(branch_t))

for i in range(analyzer_mesh.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_mesh.give_branch(i)
    lengths_mesh.append(max(branch_t) - min(branch_t))

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

for i in range(analyzer_lightcone.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_lightcone.give_branch(i)
    lengths_lightcone.append(max(branch_t) - min(branch_t))

for i in range(analyzer_mesh.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_mesh.give_branch(i)
    lengths_mesh.append(max(branch_t) - min(branch_t))

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

for i in range(analyzer_lightcone.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_lightcone.give_branch(i)
    lengths_lightcone.append(max(branch_t) - min(branch_t))

for i in range(analyzer_mesh.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_mesh.give_branch(i)
    lengths_mesh.append(max(branch_t) - min(branch_t))

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

for i in range(analyzer_lightcone.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_lightcone.give_branch(i)
    lengths_lightcone.append(max(branch_t) - min(branch_t))

for i in range(analyzer_mesh.nr_of_branches()):
    branch_t, _, _, _, _ = analyzer_mesh.give_branch(i)
    lengths_mesh.append(max(branch_t) - min(branch_t))


fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)
ax1.hist(lengths_lightcone, bins=25)
ax1.set_xlabel(r'Time length of the branch $(s)$')
ax1.set_ylabel(r'Number of branches')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)
ax2.hist(lengths_mesh, bins=25)
ax2.set_xlabel(r'Time length of the branch $(s)$')
ax2.set_ylabel(r'Number of branches')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/timelength_data_' + dataname + '.png', bbox_inches='tight')
