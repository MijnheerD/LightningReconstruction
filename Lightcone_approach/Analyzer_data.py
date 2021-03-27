"""
The d_cut parameter is a fine-tuning parameter, that depends on the dataset considered.
#1 : d_cut=400
#2 : d_cut=1000
#3 : d_cut=600
#4 : d_cut=1000
"""

import numpy as np
from Lightcone_approach.LightningAnalyzer import Analyzer

data = np.genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

dataname = 'subset_1'
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

analyzer = Analyzer(xcut, ycut, zcut, tcut, -1, weights=(1, 0), d_cut=1000)
analyzer.load_tree_from_file("Data_"+dataname+".pickle")

analyzer.render_tree()
analyzer.plot_tree()
analyzer.line_plot()
