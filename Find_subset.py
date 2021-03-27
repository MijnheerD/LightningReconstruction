import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm


data = np.genfromtxt("Data/data.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > 6000
xmax = x < 10000
ymin = y > -13000
ymax = y < -10000
zmin = z > 0
zmax = z < 4000
tmin = t > 1.15
tmax = t < 1.17
selection = zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

fig = plt.figure(1, figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

cmap = cm.plasma
norm = col.Normalize(vmin=min(tcut), vmax=max(tcut))
ax.scatter(xcut, ycut, zcut, marker='o', c=tcut, cmap=cmap, norm=norm)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Overlap of the selection with the original data')

fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
plt.show()
