"""
The d_cut parameter is a fine-tuning parameter, that depends on the dataset considered.
#1 : d_cut=400
#2 : d_cut=1000
#3 : d_cut=600
"""

import numpy as np
from Lightcone_approach.LightningAnalyzer import Analyzer

data = np.genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > 4000
xmax = x < 10000
ymin = y > -20000
ymax = y < 0
zmin = z > 0
zmax = z < 3000
tmin = t > 0.85
tmax = t < 1
selection = zmin * zmax * xmin * xmax * ymin * ymax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer = Analyzer(xcut, ycut, zcut, tcut, -1, weights=(1, 0), d_cut=400)

# analyzer.label()
analyzer.identify_data()

# analyzer.render_tree()
# analyzer.plot_tree()
# analyzer.save_tree_to_file("Data.pickle")
