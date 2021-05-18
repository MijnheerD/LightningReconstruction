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

points_lightcone = []
points_mesh = []

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
    node, _ = analyzer_lightcone.give_branch_ind(i)
    points_lightcone.append(len(node))

for i in range(analyzer_mesh.nr_of_branches()):
    node, _ = analyzer_mesh.give_branch_ind(i)
    points_mesh.append(len(node))
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
    node, _ = analyzer_lightcone.give_branch_ind(i)
    points_lightcone.append(len(node))

for i in range(analyzer_mesh.nr_of_branches()):
    node, _ = analyzer_mesh.give_branch_ind(i)
    points_mesh.append(len(node))

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
    node, _ = analyzer_lightcone.give_branch_ind(i)
    points_lightcone.append(len(node))

for i in range(analyzer_mesh.nr_of_branches()):
    node, _ = analyzer_mesh.give_branch_ind(i)
    points_mesh.append(len(node))
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
    node, _ = analyzer_lightcone.give_branch_ind(i)
    points_lightcone.append(len(node))

for i in range(analyzer_mesh.nr_of_branches()):
    node, _ = analyzer_mesh.give_branch_ind(i)
    points_mesh.append(len(node))


fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)
ax1.hist(points_lightcone, bins=30, align='left')
'''
ax1.hist(points_lightcone, bins=np.linspace(0, 450, 45), align='mid', histtype='step', linestyle='dashed',
         color='black', label='Light cone algorithm')
ax1.hist(points_mesh, bins=np.linspace(0, 450, 45), align='mid', histtype='step', linestyle='dotted',
         color='red', label='Voxel algorithm')
'''
ax1.set_xlim(left=0, right=450)
ax1.set_ylim(top=12)
ax1.set_xlabel(r'Number of points inside the branch')
ax1.set_ylabel(r'Number of branches')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)
ax2.hist(points_mesh, bins=30, align='left')
ax2.set_xlim(left=0, right=450)
ax2.set_ylim(top=12)
ax2.set_xlabel(r'Number of points inside the branch')
ax2.set_ylabel(r'Number of branches')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/points_srcs18_' + dataname + '.png', bbox_inches='tight')
