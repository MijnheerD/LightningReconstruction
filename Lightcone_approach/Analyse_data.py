import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from Lightcone_approach.Lightcone_search_one_direction import Tracker


data = np.genfromtxt("data_test.txt", delimiter=",")
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

# Make sure data is sorted by time
txyz = sorted(zip(tcut, xcut, ycut, zcut))
t_sorted, x_sorted, y_sorted, z_sorted = map(np.array, zip(*list(txyz)))

START = np.argmax(tcut)
search = Tracker(x_sorted, y_sorted, z_sorted, t_sorted, START, (1, 0), 700, direction=-1, max_points=200)
search.run()

fig = plt.figure(1, figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

cmap = cm.plasma
norm = col.Normalize(vmin=min(tcut), vmax=max(tcut))
ax.scatter(xcut, ycut, zcut, marker='^', c=tcut, cmap=cmap, norm=norm)
ax.plot([xcut[ind] for ind in search.pool], [ycut[ind] for ind in search.pool], [zcut[ind] for ind in search.pool],
        marker='o', c='navy', fillstyle='none')
ax.plot(xcut[START], ycut[START], zcut[START],
        marker='o', c='lime', fillstyle='none')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Overlap of the selection with the original data')

fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
plt.show()
