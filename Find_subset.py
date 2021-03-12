import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm


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
zmax = z < 3000
tmin = t > 0.85
tmax = t < 1
selection = zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax

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
ax.set_title('Overlap of the selection with the original data')


ax2.scatter(tcut, zcut, marker='o', c=tcut, cmap=cmap, norm=norm)
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Height [m]')
ax2.set_title('Time vs height plot of the selection')

fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
plt.show()
