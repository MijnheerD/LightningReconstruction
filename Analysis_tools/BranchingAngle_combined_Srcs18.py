import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from Lightcone_approach.LightningAnalyzer import Analyzer as LightningAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer


def angle(n, x_list, y_list, z_list):
    number = min(len(n.children[0]), len(n.children[1]), 10)
    indices_0 = sorted(n.children[0])[:number]
    indices_1 = sorted(n.children[1])[:number]
    data_0 = np.concatenate((x_plot[indices_0, np.newaxis],
                             y_plot[indices_0, np.newaxis],
                             z_plot[indices_0, np.newaxis]),
                            axis=1)
    data_1 = np.concatenate((x_plot[indices_1, np.newaxis],
                             y_plot[indices_1, np.newaxis],
                             z_plot[indices_1, np.newaxis]),
                            axis=1)
    # Calculate the mean of the points, i.e. the 'center' of the cloud
    datamean_0 = data_0.mean(axis=0)
    datamean_1 = data_1.mean(axis=0)

    # Do an SVD on the mean-centered data.
    _, _, vv_0 = np.linalg.svd(data_0 - datamean_0)
    _, _, vv_1 = np.linalg.svd(data_1 - datamean_1)

    # Calculate the angle between the direction vectors vv[0]
    inner = np.inner(vv_0[0], vv_1[0])
    norms = np.linalg.norm(vv_0) * np.linalg.norm(vv_1)

    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    deg = np.rad2deg(rad)

    return deg


data = np.genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

dataname = 'combined'

angles_lightcone = []
angles_mesh = []

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

x_plot = np.array(analyzer_lightcone.get_x())
y_plot = np.array(analyzer_lightcone.get_y())
z_plot = np.array(analyzer_lightcone.get_z())

for i in range(analyzer_lightcone.nr_of_branches()):
    node, leaf = analyzer_lightcone.give_branch_ind(i)
    if not leaf:
        angles_lightcone.append(angle(node, x_plot, y_plot, z_plot))

for i in range(analyzer_mesh.nr_of_branches()):
    node, leaf = analyzer_mesh.give_branch_ind(i)
    if not leaf:
        angles_mesh.append(angle(node, x_plot, y_plot, z_plot))
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

x_plot = np.array(analyzer_lightcone.get_x())
y_plot = np.array(analyzer_lightcone.get_y())
z_plot = np.array(analyzer_lightcone.get_z())

for i in range(analyzer_lightcone.nr_of_branches()):
    node, leaf = analyzer_lightcone.give_branch_ind(i)
    if not leaf:
        angles_lightcone.append(angle(node, x_plot, y_plot, z_plot))

for i in range(analyzer_mesh.nr_of_branches()):
    node, leaf = analyzer_mesh.give_branch_ind(i)
    if not leaf:
        angles_mesh.append(angle(node, x_plot, y_plot, z_plot))

fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)
ax1.hist(angles_lightcone, bins=np.linspace(40, 140, 200))
ax1.set_xlim([40, 140])
ax1.set_ylim([0, 3])
ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax1.set_xlabel(r'Angle between splitting branches $(\degree)$')
ax1.set_ylabel(r'Density')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)
ax2.hist(angles_mesh, bins=np.linspace(40, 140, 200))
ax2.set_xlim([40, 140])
ax2.set_ylim([0, 3])
ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax2.set_xlabel(r'Angle between splitting branches $(\degree)$')
ax2.set_ylabel(r'Density')
ax2.set_title(r'Voxel algorithm')

fig.savefig('Figures/branching_angle_srcs18_' + dataname + '.png', bbox_inches='tight')
