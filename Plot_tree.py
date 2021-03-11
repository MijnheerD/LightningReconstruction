import pickle
import matplotlib.pyplot as plt
from Lightcone_approach.LightningAnalyzer import ListNode
from anytree import LevelGroupOrderIter


tree = ListNode('root')
f = open('Lightcone_approach/Pickle_saves/Data_subset_1.pickle', 'rb')
tree = pickle.load(f)

nodes_per_level = [tup for tup in LevelGroupOrderIter(tree)]

n = len(nodes_per_level)
min_displacement = 10

x = [1,2,3,4,5]
y = [1,2,3,4,5]

fig = plt.figure(3, figsize=(10, 5))
ax = fig.add_subplot(111)

plt.plot(x, y)

ax.set_axis_off()
plt.show()
