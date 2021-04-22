"""
Make a histogram of the number of points per branch
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

points = []
for i in range(analyzer.nr_of_branches()):
    node = analyzer.give_branch_ind(i)
    points.append(len(node))

plt.hist(points, align='left')
plt.xlabel(r'Number of points per branch')
plt.ylabel(r'Density')
plt.savefig('Figures/points_data_'+dataname+'.png')
