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

distances_lightcone = []
altitudes_lightcone = []
distances_mesh = []
altitudes_mesh = []

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
ax1 = fig.add_subplot(121, projection='3d')
hist, xedges, yedges = np.histogram2d(distances_lightcone, altitudes_lightcone, bins=20)

# Construct arrays for the anchor positions of the 16 bars.
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0

# Construct arrays with the dimensions for the 16 bars.
dx = (max(distances_lightcone) - min(distances_lightcone)) / 20 * np.ones_like(zpos)
dy = (max(altitudes_lightcone) - min(altitudes_lightcone)) / 20 * np.ones_like(zpos)
dz = hist.ravel()

ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
ax1.set_xlabel(r"Distance between subsequent points (m)")
ax1.set_ylabel(r"Average of the altitudes (m)")
ax1.set_zlabel(r"Number of occurrences")

ax2 = fig.add_subplot(122, projection='3d')
hist, xedges, yedges = np.histogram2d(distances_mesh, altitudes_mesh, bins=20)

# Construct arrays for the anchor positions of the 16 bars.
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0

# Construct arrays with the dimensions for the 16 bars.
dx = (max(distances_mesh) - min(distances_mesh)) / 20 * np.ones_like(zpos)
dy = (max(altitudes_mesh) - min(altitudes_mesh)) / 20 * np.ones_like(zpos)
dz = hist.ravel()

ax2.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
ax2.set_xlabel(r"Distance between subsequent points (m)")
ax2.set_ylabel(r"Average of the altitudes (m)")
ax2.set_zlabel(r"Number of occurrences")

fig.savefig('Figures/pda_data_' + dataname + '.png')
