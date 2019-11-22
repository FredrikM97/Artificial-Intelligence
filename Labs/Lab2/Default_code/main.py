import path_planning as pp
import matplotlib.pyplot as plt
import numpy as np
from algorithms import BFS,DFS,Random


def structData(data,val):
    algorithm_map = _map_
    for keys in data.items():
        algorithm_map[keys[0][0]][keys[0][1]] = keys[1]['cost']

    algorithm_map[goal[0]][goal[1]]=val*10
    algorithm_map[start[0]][start[1]]=val*5
    
    #staticPlot(algorithm_map)
    dynamPlot(data, start,goal)
    
def staticPlot(algorithm_map):
    plt.figure()
    plt.imshow(algorithm_map)

def dynamPlot(data,start,goal,n=5):
    import matplotlib.cm as cm
    colorCode = len(data.values())
    cmap = cm.rainbow(np.linspace(0.0, 10/(colorCode + 10), colorCode))

    plt.ion()  # make show non-blocking
    plt.figure()
    plt.show() # show the figure
    axes = plt.gca()
    axes.set_xlim([0,60])
    axes.set_ylim([0,60])
    #plt.axis([0, 10, 0, 1])
    plt.scatter(start[0], start[1],color='m')
    plt.scatter(goal[0], goal[1],color='c')
    cnt = 0
    for keys in data.items():
        cnt+= 1
        plt.scatter(keys[0][0], keys[0][1],color=cmap[keys[1]['cost']])
        
        if cnt % 10 * keys[1]['cost'] == 0:
            plt.draw() 
            plt.pause(0.1)  # give the gui time to process the draw events

_map_ = pp.generateMap2d([60,60])


start, goal = tuple(np.argwhere(_map_ == -2)[0]), tuple(np.argwhere(_map_ == -3)[0])
print("Start value: ",start)

#print(nodes)
#structData(BFS.search(_map_, start, goal),-1)
#structData(DFS.search(_map_, start, goal),1)
structData(Random.search(_map_, start, goal),-1)

plt.show()