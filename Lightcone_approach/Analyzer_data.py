"""
The d_cut=400 seems to be the limit currently, to have a sensible result.
"""

import numpy as np
from Lightcone_approach.LightningAnalyzer import Analyzer

data = np.genfromtxt("data_test.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

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

analyzer = Analyzer(xcut, ycut, zcut, tcut, -1, d_cut=400)
analyzer.label()
analyzer.render_tree()
analyzer.save_tree_to_file('save_tree.txt')
