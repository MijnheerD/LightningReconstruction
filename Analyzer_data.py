"""
The d_cut parameter is a fine-tuning parameter, that depends on the dataset considered.
#1 : d_cut=400
#2 : d_cut=1000
#3 : d_cut=600
#4 : d_cut=1000

Idem for the min/max voxel size
#1 : min = 50, max=200
#2 : min = 50, max=300
#3 : min = 50, max>=200
#4 : min = 50, max=100/200
"""

from numpy import genfromtxt
from Lightcone_approach.LightningAnalyzer import Analyzer as LightconeAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer

data = genfromtxt("Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

dataname = 'Data_subset_4'
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

# analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
# analyzer_lightcone.label()
# analyzer_lightcone.save_tree_to_file(dataname+".pickle")
# analyzer_lightcone.line_plot(dataname)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=300)
analyzer_mesh.label()
analyzer_mesh.save_tree_to_file(dataname+".pickle")
analyzer_mesh.line_plot(dataname)
