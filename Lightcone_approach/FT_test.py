import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from Lightcone_approach.LightningAnalyzer import Analyzer
from anytree.search import findall_by_attr

BRANCH = 11
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
analyzer.plot_FT()

'''
grid = np.array([tcut, xcut, ycut, zcut])
fgrid = np.fft.fftn(grid)
ft = fgrid[0, :]
fx = fgrid[1, :]
fy = fgrid[2, :]
fz = fgrid[3, :]

node = findall_by_attr(analyzer.tree, 'n'+str(BRANCH))
x = [xcut[ind] for ind in node[0]]
y = [ycut[ind] for ind in node[0]]
z = [zcut[ind] for ind in node[0]]
t = [tcut[ind] for ind in node[0]]

grid2 = np.array([t, x, y, z])
fgrid2 = np.fft.fftn(grid2)
ft2 = fgrid2[0, :]
fx2 = fgrid2[1, :]
fy2 = fgrid2[2, :]
fz2 = fgrid2[3, :]

fig = plt.figure(1, figsize=(10, 10))
ax = fig.add_subplot(121, projection='3d', xlim=[0, 1e5], ylim=[0, 5e4])
ax2 = fig.add_subplot(122, projection='3d', xlim=[0, 1e5], ylim=[0, 5e4])

cmap = cm.plasma
norm = col.Normalize(vmin=min(abs(ft)), vmax=max(abs(ft)))

ax.scatter(abs(fx), abs(fy), abs(fz), marker='o', c=abs(ft), cmap=cmap, norm=norm)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax2.scatter(abs(fx2), abs(fy2), abs(fz2), marker='o', c=abs(ft2), cmap=cmap, norm=norm)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')

fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
plt.show()
'''
