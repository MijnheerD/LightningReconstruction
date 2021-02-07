import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm


data = np.genfromtxt("../Data/data_test.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

xmin = x > -4500
xmax = x < -3000
ymin = y > -8500
ymax = y < -5000
zmin = z > 3000
zmax = z < 5000
selection = zmin * zmax * xmin * xmax * ymin * ymax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

grid = np.array([tcut, xcut, ycut, zcut])
fgrid = np.fft.fftn(grid)
ft = fgrid[0, :]
fx = fgrid[1, :]
fy = fgrid[2, :]
fz = fgrid[3, :]

fig = plt.figure(1, figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

cmap = cm.plasma
norm = col.Normalize(vmin=min(abs(ft)), vmax=max(abs(ft)))
ax.scatter(abs(fx), abs(fy), abs(fz), marker='o', c=abs(ft), cmap=cmap, norm=norm)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
plt.show()
