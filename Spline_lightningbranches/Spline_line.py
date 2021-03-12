import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

data = np.genfromtxt("../Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > 6000
xmax = x < 10000
ymin = y > -7000
ymax = y < -6000
zmin = z > 0
zmax = z < 1700
tmin = t > 0.85
tmax = t < 1
selection = zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

tck, u = interpolate.splprep([xcut, ycut, zcut], s=2)
x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
u_fine = np.linspace(0, 1, 100)
x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')

ax3d.scatter(xcut, ycut, zcut)
ax3d.plot(x_fine, y_fine, z_fine, 'g')

fig2.show()
plt.show()
