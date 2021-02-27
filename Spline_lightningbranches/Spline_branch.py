import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from Lightcone_approach.LightningAnalyzer import Analyzer


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

analyzer = Analyzer(xcut, ycut, zcut, tcut, -1, weights=(1, 0), d_cut=400)
analyzer.label()
analyzer.render_tree()

t_branch, x_branch, y_branch, z_branch = analyzer.give_branch(11)
t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(sorted(zip(t_branch, x_branch, y_branch, z_branch)))))
tck, u = interpolate.splprep([x_sorted, y_sorted, z_sorted], s=100)
x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
u_fine = np.linspace(0, 1, 100)
x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')

ax3d.scatter(x_branch, y_branch, z_branch)
ax3d.plot(x_fine, y_fine, z_fine, 'g')

fig2.show()
plt.show()
