import numpy as np
import matplotlib.pyplot as plt
from algorithms import uninformedSearch as uS
from algorithms import informedSearch as iS
from plotting import Plotting
import path_planning as pp
import matplotlib.pyplot as plt


def pathFunc(newMap, goal):
    example_solved_path = [[],[]]
    node = newMap[goal]
    cords = goal
    print("Hurr durr hurr: ", node)
    while node['cost'] > 0:
        example_solved_path[1].insert(0,cords[0])
        example_solved_path[0].insert(0,cords[1])
        node = newMap[node['parent']]
        cords = node['parent']
    return example_solved_path

def mapFunc(_map_, newMap):
    example_solved_map = _map_
    for keys in newMap.items():
        if example_solved_map[keys[0][0],keys[0][1]] >=0:
            example_solved_map[keys[0][0],keys[0][1]] = int(keys[1]['cost'])
    return example_solved_map

def main():  
    #_map_ = pp.generateMap2d([60,60])
    _map_ = pp.generateMap2d_obstacle([60,60])[0]
    start, goal = tuple(np.argwhere(_map_ == -2)[0]), tuple(np.argwhere(_map_ == -3)[0])
    print("Start value: ",start, " Goal value: ", goal)
    
    mapObj = Plotting(_map_, start, goal)

    #for x in range(0,3):
        # Get the new map from the search algorithm, Search Type [0: BFS, 1: DFS, 2: Random]
    for x in range(0,4):
        newMap = iS.search(_map_, start, goal, x)

    # Display result directly
    #dp.staticPlot(newMap,_map_, start, goal,-1)

    # Dynamically draw the map

        pp.plotMap(mapFunc(_map_, newMap),pathFunc(newMap, goal))
    #mapObj.dynamPlot(newMap)
    #mapObj.dynamPlot(newMap)

main()