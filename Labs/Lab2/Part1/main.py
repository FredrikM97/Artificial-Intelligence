import numpy as np
import matplotlib.pyplot as plt
from algorithms import uninformedSearch as uS
from algorithms import informedSearch as iS
from plotting import Plotting
import path_planning as pp
    
def main():  
    #_map_ = pp.generateMap2d([60,60])
    _map_ = pp.generateMap2d_obstacle([60,60])[0]
    start, goal = tuple(np.argwhere(_map_ == -2)[0]), tuple(np.argwhere(_map_ == -3)[0])
    print("Start value: ",start, " Goal value: ", goal)
    
    mapObj = Plotting(_map_, start, goal)

    #for x in range(0,3):
        # Get the new map from the search algorithm, Search Type [0: BFS, 1: DFS, 2: Random]
    newMap = iS.search(_map_, start, goal, 0)

        # Display result directly
        #dp.staticPlot(newMap,_map_, start, goal,-1)

        # Dynamically draw the map
    mapObj.dynamPlot(newMap)
    #mapObj.dynamPlot(newMap)
main()