"""
The d_cut parameter is a fine-tuning parameter, that depends on the dataset considered.
#1 : d_cut=800
#2 : d_cut=800
#3 : d_cut=200
#4 : d_cut=200
"""
import numpy as np
from Lightcone_approach.LightningAnalyzer import Analyzer

data = np.genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
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

analyzer = Analyzer(xcut, ycut, zcut, tcut, -1, weights=(1, 0), d_cut=800)
analyzer.load_tree_from_file("Data_"+dataname+".pickle")

analyzer.render_tree()
analyzer.plot_tree()
analyzer.line_plot()
