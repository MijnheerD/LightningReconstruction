from numpy import genfromtxt
from Lightcone_approach.LightningAnalyzer import Analyzer as LightconeAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer

data = genfromtxt("Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

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
analyzer_lightcone.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_lightcone.plot_tree("Data_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Data_" + dataset)
# analyzer_lightcone.plot_tree_projections("Data_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_mesh.plot_tree("Data_" + dataset, lonely=False)
analyzer_mesh.line_plot("Data_" + dataset)
# analyzer_mesh.plot_tree_projections("Data_" + dataset)

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
analyzer_lightcone.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_lightcone.plot_tree("Data_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Data_" + dataset)
# analyzer_lightcone.plot_tree_projections("Data_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_mesh.plot_tree("Data_" + dataset, lonely=False)
analyzer_mesh.line_plot("Data_" + dataset)
# analyzer_mesh.plot_tree_projections("Data_" + dataset)

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
analyzer_lightcone.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_lightcone.plot_tree("Data_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Data_" + dataset)
# analyzer_lightcone.plot_tree_projections("Data_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_mesh.plot_tree("Data_" + dataset, lonely=False)
analyzer_mesh.line_plot("Data_" + dataset)
# analyzer_mesh.plot_tree_projections("Data_" + dataset)

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
analyzer_lightcone.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_lightcone.plot_tree("Data_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Data_" + dataset)
# analyzer_lightcone.plot_tree_projections("Data_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Data_" + dataset + ".pickle")
analyzer_mesh.plot_tree("Data_" + dataset, lonely=False)
analyzer_mesh.line_plot("Data_" + dataset)
# analyzer_mesh.plot_tree_projections("Data_" + dataset)