"""
#1 : min = 50, max=200
#2 : min = 50, max=300
#3 : min = 50, max>=200
#4 : min = 50, max=100/200

#1 : min = 50, max=100
#2 : min = 50, max=100
#3 : min = 50, max=100
#4 : min = 50, max=100
"""

from numpy import genfromtxt
from Mesh_approach.LightningAnalyzer import Analyzer

data = genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

dataname = 'Srcs18_subset_4'
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

tree = Analyzer(tcut, xcut, ycut, zcut, min_voxel_size=50, max_voxel_size=200)
tree.octree.refine(min_side=50, max_side=100)
tree.octree.voxel_plot()
