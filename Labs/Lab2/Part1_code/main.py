import copy
import numpy as np
import matplotlib.pyplot as plt

from plotting import Plotting
import path_planning as pp
import matplotlib.pyplot as plt


from algorithmSearch.search import defineClass


# Add the solved path to the map
def pathFunc(newMap, goal):
    example_solved_path = [[],[]]
    node = newMap[goal]
    cords = goal
    while node['parent'] != None:
        example_solved_path[1].insert(0,cords[0])
        example_solved_path[0].insert(0,cords[1])
        node = newMap[node['parent']]
        cords = node['parent']
    return example_solved_path

# Add the searched area to the map
def mapFunc(map, newMap):
    example_solved_map = copy.copy(map)
    for keys in newMap.items():
        if example_solved_map[keys[0][0],keys[0][1]] >=0:
            example_solved_map[keys[0][0],keys[0][1]] = int(keys[1]['cost'])
    return example_solved_map
    
    
def main():  
    _map_ = pp.generateMap2d_obstacle([100,100])
    #_map_ = pp.generateMap2d([60,60])
    
    # Dummy so we can run both with and without obstacle without changing code
    if len(_map_) == 2:
        map = _map_
    else:
        map = [_map_]

    # X,Y: Wrong, someone the data is placed Y,X)
    start, goal = tuple(np.argwhere(map[0] == -2)[0]), tuple(np.argwhere(map[0] == -3)[0])
    print("Start value: ",start, " Goal value: ", goal)
    
    # Plot each algorithm
    
    for x in range(0,8):
        data = defineClass(_map_, start, goal, x)
        newMap = data[0][0]
        pp.plotMap(mapFunc(map[0], newMap),pathFunc(newMap, goal),str(data[1]) + ", g: " + str(data[0][1]))

        print(str(data[1]) + " " + str(data[0][1]))
    plt.show()
    '''
    data = defineClass(_map_, start, goal, 0)
    newMap = data[0][0]
    # Dynamic plotting - Use with care
    mapObj = Plotting(map, start, goal)
    mapObj.dynamPlot(newMap)
    '''

    
            
main()