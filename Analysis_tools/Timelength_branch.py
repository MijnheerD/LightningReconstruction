"""
Make a histogram of the time lengths of every branch in the flash
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

lengths = []
for i in range(analyzer.nr_of_branches()):
    branch_t, _, _, _ = analyzer.give_branch(i)
    lengths.append(max(branch_t) - min(branch_t))

plt.hist(lengths, align='left')
plt.xlabel(r'Time length of branches $(s)$')
plt.ylabel(r'Density')
plt.savefig('Figures/timelength_data_'+dataname+'.png')
