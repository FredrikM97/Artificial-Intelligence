import path_planning as pp
import matplotlib.pyplot as plt
import numpy as np
from algorithms import BFS

_map_ = pp.generateMap2d([60,60])
plt.clf()
plt.imshow(_map_)

start, goal = list(np.argwhere(_map_ == -2)[0]), list(np.argwhere(_map_ == -3)[0])
print(start)
BFS.search(_map_, start, goal)