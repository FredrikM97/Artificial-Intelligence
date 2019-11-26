import copy
import numpy as np
import matplotlib.pyplot as plt
from algorithms import uninformedSearch as uS
from algorithms import informedSearch as iS
from algorithms import smartSearch as sS

from search import Search

from plotting import Plotting
import path_planning as pp
import matplotlib.pyplot as plt


def pathFunc(newMap, goal):
    example_solved_path = [[],[]]
    node = newMap[goal]
    cords = goal
    while node['cost'] != 0:
        example_solved_path[1].insert(0,cords[0])
        example_solved_path[0].insert(0,cords[1])
        node = newMap[node['parent']]
        cords = node['parent']
    return example_solved_path

def mapFunc(map, newMap):
    example_solved_map = copy.copy(map)
    for keys in newMap.items():
        if example_solved_map[keys[0][0],keys[0][1]] >=0:
            example_solved_map[keys[0][0],keys[0][1]] = int(keys[1]['cost'])
    return example_solved_map

def main():  
    #_map_ = pp.generateMap2d([60,60])
    _map_ = pp.generateMap2d_obstacle([60,60])
    
    # X,Y: Wrong, someone the data is placed Y,X)
    start, goal = tuple(np.argwhere(_map_[0] == -2)[0]), tuple(np.argwhere(_map_[0] == -3)[0])
    print("Start value: ",start, " Goal value: ", goal)

    #copy_map = copy.copy(_map_)
    #pp.plotMap(copy_map[0], copy_map[0],'Map')
    mapObj = Plotting(_map_[0], start, goal)
    data = [['BFS', 'DFS', 'Random'],['Greedy - Manhattan', 'Greedy - Euklides', 'A* - Manhattan', 'A* - Euklides'],['Special']]

    #pp.plotMap(_map_[0], _map_[0],'Map')

    '''
    for x in range(0,3):
        for y in range(0,4):
            if x == 0 and y < 3:

                print("Uninformed")
                newMap = uS.search(_map_[0], start, goal, y)
                pp.plotMap(mapFunc(_map_[0], newMap),pathFunc(newMap, goal),data[x][y])
            elif x == 1:
                print("Informed")
                newMap = iS.search(_map_[0], start, goal, y) 
                pp.plotMap(mapFunc(_map_[0], newMap),pathFunc(newMap, goal),data[x][y])
            elif x == 2:
                print("Special")
                newMap = sS.search(_map_, start, goal) 
                pp.plotMap(mapFunc(_map_[0], newMap),pathFunc(newMap, goal),data[x][y])
                break
    '''             
    print("Special")
    #newMap = Search.SmartSearch(_map_, start, goal).search()
    newMap = Search(_map_, start, goal).search()
    pp.plotMap(mapFunc(_map_[0], newMap),pathFunc(newMap, goal),data[0][0])
    
    plt.show()
        # Special case
               # Uninformed
        #  # Informed
        #         # Special
    #mapObj.dynamPlot(newMap)
            
main()