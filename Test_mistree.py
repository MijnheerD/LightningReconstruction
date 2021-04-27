import mistree as mist
import matplotlib.pyplot as plt
from numpy import genfromtxt

data = genfromtxt("./Data/data.txt", delimiter=",")
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
selection = zmin * zmax * ymin * ymax * xmin * xmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

mst = mist.GetMST(x=xcut, y=ycut, z=zcut)

d, l, b, s = mst.get_stats()
l_index = mst.edge_index
b_index = mst.branch_index

fig = plt.figure(figsize=(7., 7.))
ax1 = fig.add_subplot(111, projection='3d')

# plotting nodes:
ax1.scatter(xcut, ycut, zcut, s=10, color='r')

# plotting MST edges:
for i in range(l_index.shape[1]):
    ax1.plot([xcut[l_index[0][i]], xcut[l_index[1][i]]],
             [ycut[l_index[0][i]], ycut[l_index[1][i]]],
             [zcut[l_index[0][i]], zcut[l_index[1][i]]],
             color='k')

ax1.set_xlabel(r'$X$', size=16)
ax1.set_ylabel(r'$Y$', size=16)
ax1.set_zlabel(r'$Z$', size=16)

plt.show()
