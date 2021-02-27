import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm


data = np.genfromtxt("Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
x = data[:, 1]
y = data[:, 2]
z = data[:, 3]
t = data[:, 4]

xmin = x > -100000
xmax = x < -35000
ymin = y > 10000
ymax = y < 100000
zmin = z > 0
zmax = z < 10000
tmin = t > 1.14
tmax = t < 1.18
selection = zmin * zmax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

fig = plt.figure(1, figsize=(15, 10))
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)

cmap = cm.plasma
norm = col.Normalize(vmin=min(t), vmax=max(t))

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
