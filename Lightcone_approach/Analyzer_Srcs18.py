import numpy as np
from Lightcone_approach.LightningAnalyzer import Analyzer

data = np.genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
x = data[:, 1]
y = data[:, 2]
z = data[:, 3]
t = data[:, 4]

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

analyzer = Analyzer(x, y, z, t, -1, weights=(1, 0), d_cut=400)
analyzer.identify_data()
