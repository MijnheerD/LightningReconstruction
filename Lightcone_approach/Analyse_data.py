import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Lightcone_approach.Lightcone_search import Stepper

data = np.genfromtxt("data_test.txt", delimiter=",")
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

# Make sure data is sorted by time

xmin = x > 3000
xmax = x < 7000
ymin = y > -8000
ymax = y < -6000
zmin = z > 5000
selection = xmin * xmax * ymin * ymax * zmin

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]
search = Stepper(xcut, ycut, zcut, tcut, 27, (1, 1e4), 0.1)
search.run()

'''
fig = plt.figure(1, figsize=(20, 10))
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

ax.scatter(xcut, ycut, zcut, marker='^', c='b')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Original data')

ax2.scatter([xcut[ind] for ind in search.pool], [ycut[ind] for ind in search.pool], [zcut[ind] for ind in search.pool],
            marker='o', c='r')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Data selected by lightcone algorithm')
'''

fig2 = plt.figure(2, figsize=(10, 10))
ax3 = fig2.add_subplot(111, projection='3d')

ax3.scatter(xcut, ycut, zcut, marker='^', c='b')
ax3.scatter([xcut[ind] for ind in search.pool], [ycut[ind] for ind in search.pool], [zcut[ind] for ind in search.pool],
            marker='o', c='r')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
ax3.set_title('Overlap of the selection with the original data')

plt.show()
