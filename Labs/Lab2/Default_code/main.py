import path_planning as pp
import matplotlib.pyplot as plt
import numpy as np
from algorithms import BFS

_map_ = pp.generateMap2d([60,60])
#plt.clf()
#plt.imshow(_map_)

start, goal = tuple(np.argwhere(_map_ == -2)[0]), tuple(np.argwhere(_map_ == -3)[0])
print("Start value: ",start)
nodes = BFS.search(_map_, start, goal)
#print(nodes)
algorithm_map = _map_

for keys in nodes.items():
    algorithm_map[keys[0][0]][keys[0][1]] = keys[1]['cost']

algorithm_map[goal[0]][goal[1]]=-10
algorithm_map[start[0]][start[1]]=-5
print(algorithm_map)
plt.imshow(algorithm_map)
plt.show()