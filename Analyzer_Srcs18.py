"""
The d_cut parameter is a fine-tuning parameter, that depends on the dataset considered.
#1 : d_cut=800
#2 : d_cut=800
#3 : d_cut=200
#4 : d_cut=200

Idem for the min/max voxel size.
#1 :
#2 :
#3 :
#4 :
"""

from numpy import genfromtxt
from Lightcone_approach.LightningAnalyzer import Analyzer as LightningAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer


data = genfromtxt("Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

dataname = 'Srcs18_subset_1'
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

# analyzer_lightning = LightningAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
# analyzer_lightning.label()
# analyzer_lightning.save_tree_to_file(dataname+".pickle")
# analyzer_lightning.line_plot(dataname)

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
analyzer_mesh.label()
analyzer_mesh.save_tree_to_file(dataname+".pickle")
analyzer_mesh.line_plot(dataname)
