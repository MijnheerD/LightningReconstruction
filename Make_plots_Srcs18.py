from numpy import genfromtxt
from Lightcone_approach.LightningAnalyzer import Analyzer as LightconeAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer

data = genfromtxt("Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")
analyzer_lightcone.plot_tree("Srcs18_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Srcs18_" + dataset)
# analyzer_lightcone.plot_tree_projections("Srcs18_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")
analyzer_mesh.plot_tree("Srcs18_" + dataset + "_clean", lonely=False)
analyzer_mesh.line_plot("Srcs18_" + dataset + "_clean")
# analyzer_mesh.plot_tree_projections("Srcs18_" + dataset + "_clean")

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")
analyzer_lightcone.plot_tree("Srcs18_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Srcs18_" + dataset)
# analyzer_lightcone.plot_tree_projections("Srcs18_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")
analyzer_mesh.plot_tree("Srcs18_" + dataset + "_clean", lonely=False)
analyzer_mesh.line_plot("Srcs18_" + dataset + "_clean")
# analyzer_mesh.plot_tree_projections("Srcs18_" + dataset + "_clean")

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")
analyzer_lightcone.plot_tree("Srcs18_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Srcs18_" + dataset)
# analyzer_lightcone.plot_tree_projections("Srcs18_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")
analyzer_mesh.plot_tree("Srcs18_" + dataset + "_clean", lonely=False)
analyzer_mesh.line_plot("Srcs18_" + dataset + "_clean")
# analyzer_mesh.plot_tree_projections("Srcs18_" + dataset + "_clean")

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

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataset+".pickle")
analyzer_lightcone.plot_tree("Srcs18_" + dataset, lonely=False)
analyzer_lightcone.line_plot("Srcs18_" + dataset)
# analyzer_lightcone.plot_tree_projections("Srcs18_" + dataset)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataset + "_clean" + ".pickle")
analyzer_mesh.plot_tree("Srcs18_" + dataset + "_clean", lonely=False)
analyzer_mesh.line_plot("Srcs18_" + dataset + "_clean")
# analyzer_mesh.plot_tree_projections("Srcs18_" + dataset + "_clean")
