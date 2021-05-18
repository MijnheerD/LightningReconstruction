import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import ticker
from Lightcone_approach.LightningAnalyzer import Analyzer as LightconeAnalyzer
from Mesh_approach.LightningAnalyzer import Analyzer as MeshAnalyzer


data = np.genfromtxt("../Data/Srcs18-oddSE.csv", comments='!', delimiter=",")
y = data[:, 1]
x = data[:, 2]
z = data[:, 3]
t = data[:, 4]
chi2 = data[:, 5]

dataname = 'subset_1'
xmin = x > 60000
xmax = x < 70000
ymin = y > -50000
ymax = y < -40000
zmin = z > 2000
zmax = z < 5500
tmin = t > 1.22
tmax = t < 1.30
chi2max = chi2 < 16
selection = chi2max * zmin * zmax * ymin * ymax * xmin * xmax * tmin * tmax

xcut = x[selection]
ycut = y[selection]
zcut = z[selection]
tcut = t[selection]

analyzer_lightcone = LightconeAnalyzer(tcut, xcut, ycut, zcut, -1, weights=(1, 0), d_cut=1000)
analyzer_lightcone.load_tree_from_file("Data_Srcs18_"+dataname+".pickle")

analyzer_mesh = MeshAnalyzer(tcut, xcut, ycut, zcut, min_voxel_size=100, max_voxel_size=300)
analyzer_mesh.load_tree_from_file("Srcs18_" + dataname + "_clean" + ".pickle")

events_lightcone = []
bp_lightcone = []
for i in range(analyzer_lightcone.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_lightcone.give_branch(i)
    t_0 = min(t_branch)  # np.percentile(t_branch, 1)
    bp_lightcone.append(t_0)
    events_lightcone.extend(t_branch - t_0)

events_mesh = []
bp_mesh = []
for i in range(analyzer_mesh.nr_of_branches()):
    t_branch, _, _, _, _ = analyzer_mesh.give_branch(i)
    t_0 = min(t_branch)  # np.percentile(t_branch, 1)
    bp_mesh.append(t_0)
    events_mesh.extend(t_branch - t_0)

fig = plt.figure(figsize=(16, 8))
gs = GridSpec(1, 3, figure=fig)

ax1 = fig.add_subplot(gs[0, 0])

ax1.hist(events_lightcone, align='left', bins=30)
ax1.set_ylim((0, 200))
ax1.set_xlabel(r'$t - t_0 (s)$')
ax1.set_ylabel(r'Density')
ax1.set_title(r'Light cone algorithm')

ax2 = fig.add_subplot(gs[0, 1:])

ax2.hist(events_mesh, align='left', bins=60)
ax2.set_ylim((0, 200))
ax2.set_xlabel(r'$t - t_0 (s)$')
ax2.set_ylabel(r'Density')
ax2.set_title(r'Voxel algorithm')
ax2.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

fig.savefig('Figures/ef_data_' + dataname + '.png', bbox_inches='tight')
