import mistree as mist
import matplotlib.pyplot as plt
from numpy import genfromtxt

data = genfromtxt("./Data/data.txt", delimiter=",")
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

# plotting branches:
'''
for i in range(len(b_index)):

    ax1.plot([xcut[l_index[0][b_index[i][0]]], xcut[l_index[1][b_index[i][0]]]],
             [ycut[l_index[0][b_index[i][0]]], ycut[l_index[1][b_index[i][0]]]],
             [zcut[l_index[0][b_index[i][0]]], zcut[l_index[1][b_index[i][0]]]],
             color='C0', linestyle=':')
    for j in range(1, len(b_index[i]) - 1):
        ax1.plot([xcut[l_index[0][b_index[i][j]]], xcut[l_index[1][b_index[i][j]]]],
                 [ycut[l_index[0][b_index[i][j]]], ycut[l_index[1][b_index[i][j]]]],
                 [zcut[l_index[0][b_index[i][j]]], zcut[l_index[1][b_index[i][j]]]],
                 color='C0')
    ax1.plot([xcut[l_index[0][b_index[i][-1]]], xcut[l_index[1][b_index[i][-1]]]],
             [ycut[l_index[0][b_index[i][-1]]], ycut[l_index[1][b_index[i][-1]]]],
             [zcut[l_index[0][b_index[i][-1]]], zcut[l_index[1][b_index[i][-1]]]],
             color='C0', linestyle=':')
'''
# plotting MST edges:
for i in range(l_index.shape[1]):
    ax1.plot([xcut[l_index[0][i]], xcut[l_index[1][i]]],
             [ycut[l_index[0][i]], ycut[l_index[1][i]]],
             [zcut[l_index[0][i]], zcut[l_index[1][i]]],
             color='grey', linewidth=1, alpha=1)

ax1.plot([], [], color='C0', label=r'$Branch$ $Mid$')
ax1.plot([], [], color='C0', label=r'$Branch$ $End$', linestyle=':')
ax1.plot([], [], color='grey', alpha=0.25, label=r'$MST$ $Edges$')

ax1.set_xlabel(r'$X$', size=16)
ax1.set_ylabel(r'$Y$', size=16)
ax1.set_zlabel(r'$Z$', size=16)
# ax1.legend(loc='best')

plt.tight_layout()
plt.show()
