"""
Make a histogram of the number of branches vs altitude
"""

import numpy as np
import matplotlib.pyplot as plt
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

analyzer = Analyzer(xcut, ycut, zcut, tcut, -1, weights=(1, 0), d_cut=400)
analyzer.load_tree_from_file("Data_"+dataname+".pickle")


nr_of_bins = 50
bin_size = (max(zcut) - min(zcut))/nr_of_bins  # m
branch_altitudes = []
for i in range(analyzer.nr_of_branches()):
    _, _, _, branch_z = analyzer.give_branch(i)
    branch_altitudes.extend(np.arange(min(branch_z), max(branch_z), bin_size))

plt.hist(branch_altitudes, align='left', bins=nr_of_bins)
plt.xlabel(r'Altitude $(m)$')
plt.ylabel(r'Density')
plt.savefig('Figures/branching_data_' + dataname + '.png')
