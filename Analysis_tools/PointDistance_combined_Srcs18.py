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

distances_lightcone = []
altitudes_lightcone = []
distances_mesh = []
altitudes_mesh = []

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
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_lightcone.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_lightcone.extend(distances)
    altitudes_lightcone.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_mesh.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_mesh.extend(distances)
    altitudes_mesh.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)

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
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_lightcone.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_lightcone.extend(distances)
    altitudes_lightcone.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_mesh.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_mesh.extend(distances)
    altitudes_mesh.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)

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
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_lightcone.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_lightcone.extend(distances)
    altitudes_lightcone.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_mesh.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_mesh.extend(distances)
    altitudes_mesh.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)

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
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_lightcone.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_lightcone.extend(distances)
    altitudes_lightcone.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)

for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, x_branch, y_branch, z_branch, _ = analyzer_mesh.give_branch(i)
    txyz = sorted(zip(t_branch, x_branch, y_branch, z_branch))
    t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))
    dx = x_sorted[1:] - x_sorted[:-1]
    dy = y_sorted[1:] - y_sorted[:-1]
    dz = z_sorted[1:] - z_sorted[:-1]
    distances = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    distances_mesh.extend(distances)
    altitudes_mesh.extend(abs(z_sorted[1:] + z_sorted[:-1]) / 2)


fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121)
hist, xedges, yedges = np.histogram2d(distances_lightcone, altitudes_lightcone,
                                      bins=[np.arange(min(distances_lightcone), max(distances_lightcone), 25),
                                            np.arange(min(altitudes_lightcone), max(altitudes_lightcone), 200)])
xpos, ypos = np.meshgrid(xedges[:-1] + (xedges[1]-xedges[0])/2, yedges[:-1] + (yedges[1]-yedges[0])/2, indexing="ij")

pcm1 = ax1.pcolormesh(xpos, ypos, hist, shading='auto')
ax1.set_xlim(left=0, right=400)
ax1.set_ylim(top=6400)
ax1.set_xlabel(r"Distance between subsequent points (m)")
ax1.set_ylabel(r"Average of the altitudes (m)")
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(122)
hist, xedges, yedges = np.histogram2d(distances_mesh, altitudes_mesh,
                                      bins=[np.arange(min(distances_mesh), max(distances_mesh), 25),
                                            np.arange(min(altitudes_mesh), max(altitudes_mesh), 200)])
xpos, ypos = np.meshgrid(xedges[:-1] + (xedges[1]-xedges[0])/2, yedges[:-1] + (yedges[1]-yedges[0])/2, indexing="ij")

pcm2 = ax2.pcolormesh(xpos, ypos, hist, shading='auto')
ax2.set_xlim(left=0, right=400)
ax2.set_ylim(top=6400)
ax2.set_xlabel(r"Distance between subsequent points (m)")
ax2.set_ylabel(r"Average of the altitudes (m)")
ax2.set_title(r'Voxel algorithm')

fig.colorbar(pcm1, ax=ax1)
fig.colorbar(pcm2, ax=ax2)
fig.savefig('Figures/pda_srcs18_' + dataname + '.png')
