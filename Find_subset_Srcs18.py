import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm


data = np.genfromtxt("Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
x = data[:, 2]
y = data[:, 1]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

xmin = x > 60000
xmax = x < 70000
ymin = y > -50000
ymax = y < -40000
zmin = z > 2000
zmax = z < 5500
tmin = t > 1.14
tmax = t < 1.18
chi2max = chi2 < 16
selection = chi2max * zmin * zmax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

fig = plt.figure(1, figsize=(15, 10))
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)

cmap = cm.plasma
norm = col.Normalize(vmin=min(tcut), vmax=max(tcut))

ax.scatter(xcut, ycut, zcut, marker='o', c=tcut, cmap=cmap, norm=norm)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Selection of the data')

ax2.scatter(tcut, zcut, marker='o', c=tcut, cmap=cmap, norm=norm)
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Height [m]')
ax2.set_title('Time vs height plot of the selection')

fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
plt.show()
