import numpy as np
import matplotlib.pyplot as plt
from Mesh_approach.Mesh_fixed_res import Analyzer

data = np.genfromtxt("../Data/data.txt", delimiter=",")
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


resolution = 1000
# space = Space(tcut, xcut, ycut, zcut, resolution)
# space.plot_split()

analyzer = Analyzer(tcut, xcut, ycut, zcut, resolution)
coarse, fine = analyzer.run()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(coarse, label='Coarse')
ax.plot(fine, label='Fine')
ax.legend()
plt.show()
