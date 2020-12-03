import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from Lightcone_approach.LightiningAnalyzer import Analyzer

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

analyzer = Analyzer(xcut, ycut, zcut, tcut, -1)
analyzer.label()
analyzer.render_tree()

branch = analyzer.tree.children[0]

fig = plt.figure(1, figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

cmap = cm.plasma
norm = col.Normalize(vmin=min(tcut), vmax=max(tcut))
ax.scatter(xcut, ycut, zcut, marker='^', c=tcut, cmap=cmap, norm=norm)
ax.scatter([xcut[ind] for ind in branch], [ycut[ind] for ind in branch], [zcut[ind] for ind in branch],
           marker='o', c='navy')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Overlap of the selection with the original data')

fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
plt.show()
