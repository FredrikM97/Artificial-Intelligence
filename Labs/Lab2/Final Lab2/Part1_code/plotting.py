import path_planning as pp
import matplotlib.pyplot as plt
import numpy as np
class Plotting:
    def __init__(self, _map_, start, goal):
        self.map = _map_[0] 
        self.mapSize = [len(self.map[0]), len(self.map[0])]
        #self.terrain = self.createTerrain()
        self.start = start
        self.goal = goal

    # Depricated
    def createTerrain(self):
        for keys1 in range(0,self.mapSize[0]):
            for keys2 in range(0,self.mapSize[1]):
                
                keys1,keys2 = int(keys1),int(keys2)

                pos = self.map[keys1][keys2]
                if pos == -1:
                    plt.scatter(keys1, keys2,color='r')
                elif pos == -2:
                    plt.scatter(keys1, keys2,color='m')
                elif pos == -3:
                    plt.scatter(keys1, keys2,color='c')
        return 
        
    # Parameters: The new map, the old map, start and goal positions, value depending on BFS or DFS
    # Map struct: [[],[],[]]
    def staticPlot(self,newMap, val):
        algorithm_map = self.map

        for keys in newMap.items():
            algorithm_map[keys[0][0]][keys[0][1]] = keys[1]['cost']

        algorithm_map[self.goal[0]][self.goal[1]]=val*10
        algorithm_map[self.start[0]][self.start[1]]=val*5

        plt.figure()
        plt.imshow(algorithm_map)

    # Parameters: Map to be plotted, Start: tuple of cords, Goal: Tuple of cords, n: batch size for plotting 
    # Map struct: [[],[],[]]
    def dynamPlot(self,newMap,n=5):
        import matplotlib.cm as cm
        colorCode = len(newMap.values())
        cmap = cm.rainbow(np.linspace(0.0, 10/(colorCode + 10), colorCode))

        #fig = plt.figure() 
        #plt.figure()
        plt.clf
        axes=plt.gca()  
        axes.set_xlim([0,len(self.map)])
        axes.set_ylim([0,len(self.map[0])])                          
        axes.set_ylim(axes.get_ylim()[::-1])  
        
        self.createTerrain()
        plt.ion()  # make show non-blocking
        plt.show() # show the figure

              
        #axes.xaxis.tick_top()                      
        #axes.yaxis.tick_top()         
        
        #plt.imshow(self.map) #Destoys the map
        #plt.axis([0, 10, 0, 1])
        plt.scatter(self.start[0], self.start[1], color='b')
        plt.scatter(self.goal[0], self.goal[1], color='c')
        cnt = 0

        for keys in newMap.items():
            cnt+= 1
            plt.scatter(keys[0][0], keys[0][1],color='g')#cmap[keys[1]['cost']])#
        
            if cnt % 10 * keys[1]['cost'] == 0:
                plt.draw() 
                plt.pause(0.1)  # give the gui time to process the draw events
    

        node = newMap[self.goal]
        cords = self.goal
        while node['cost'] != 0:
            plt.scatter(cords[0], cords[1],color="y")
            node = newMap[node['parent']]
            cords = node['parent']
        #plt.show() # show the figure
        plt.pause(30)
