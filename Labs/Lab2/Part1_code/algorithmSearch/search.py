import numpy as np
from importlib import import_module

from .classes import Special, Random, BFS, DFS, Astar_euc, Astar_man,Greedy_euc, Greedy_man 

accessable_classes = [    
    BFS,
    DFS, 
    Random, 
    Greedy_euc, 
    Greedy_man,
    Astar_euc, 
    Astar_man, 
    Special
]

def defineClass(_map_, start, goal,type):
    
    class Search(accessable_classes[type]):
        def __init__(self, map, start, goal):
            super().__init__()
            self.start = start # Start position
            self.goal = goal # TO search for
            self.map = map

        def search(self):
            
            self.frontier.add(self.start,0)
            self.addNode(None,self.start, 0) 
            # if there is still nodes to open
            while not self.frontier.isEmpty():
                current = self.frontier.remove()
                # check if the goal is reached
                if np.array_equal(current,self.goal):
                    print("Found the goal!!")
                    self.g = self.calculatePathCost()
                    break


                for obj in self.get_neighbors(list(current)).items():   

                    # If object is an obstacle dont add it to the queue

                    if obj[1] == -1:
                        continue
                        
                    else:

                        cost = self.cost_function(obj[0], current)

                        # add next cell to open list
                        if not self.exists(obj[0]):
                            self.frontier.add(obj[0], cost)

                        # add to path
                        self.addNode(current,obj[0], cost) 
                
            return [self.node, self.g]

        def get_neighbors(self,current):
            # Get the neighbors around
            x = current[0]
            y = current[1]
            
            info = {}
            # Get all the items from the four directions
            paths = [(x-1,y), (x+1,y),(x,y+1), (x,y-1)]

            if len(self.map) == 2:
                map = self.map[0]
            else: 
                map = self.map
            
            maplen = len(map)
    

            for pos in paths:
                con1 = pos[0] >= 0 and pos[1] >= 0
                con2 = pos[0] < maplen and pos[1] < maplen
                if con1 and con2:
                    info[pos] = int(map[[pos[0]],[pos[1]]][0])

            return info   

        def int2str(self,val1,val2):
            return tuple([val1,val2])

        def calculatePathCost(self):
    
            g = 0
            node = self.getNode(self.goal)
            while node['parent'] != None:
                g += 1
                node = self.getNode(node['parent'])

            return g

    return [Search(_map_, start, goal).search(), accessable_classes[type].__name__]