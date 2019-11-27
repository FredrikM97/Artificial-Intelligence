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

def defineClass(_map_, start, goal,type, depthLimit=-1):
    
    class Search(accessable_classes[type]):
        def __init__(self, map, start, goal, depthLimit):
            super().__init__()
            self.start = start # Start position
            self.goal = goal # TO search for
            self.map = map
            self.steps = 0
            self.depthLimit = depthLimit
            self.g = 0

        def search(self):
            
            self.frontier.add(self.start,0)
            self.addNode(None,self.start, 0, 0) 
            # if there is still nodes to open
            while not self.frontier.isEmpty():
                current = self.frontier.remove()
                
                # If Maximum depth is reached
                if not self.depthLimit == -1 and self.depthLimit <= self.node[current]['g'] or np.array_equal(current,self.goal):
                    self.g = self.node[current]['g']
                    break
                self.steps += 1

                # Start checking each node
                for obj in self.get_neighbors(list(current)).items():   
                    
                    cost = self.cost_function(obj[0], current)

                    # add next cell to open list
                    if not self.exists(obj[0]):
                        self.frontier.add(obj[0], cost)
        
                    # add to path
                    self.addNode(current,obj[0], cost, self.node[current]['g'] + 1) 
                
            return [self.node, self.g, self.steps]

        def get_neighbors(self,current):
            # Get the neighbors around
            x = current[0]
            y = current[1]
            
            info = {}
            # Get all the items from the four directions
            paths = [(x-1,y), (x+1,y),(x,y+1), (x,y-1)]

            map = self.mapType()
            
            maplen = len(map)
    

            for pos in paths:
                con1 = pos[0] >= 0 and pos[1] >= 0
                con2 = pos[0] < maplen and pos[1] < maplen
                if con1 and con2 and map[[pos[0]],[pos[1]]][0] != -1:
                    info[pos] = int(map[[pos[0]],[pos[1]]][0])

            return info
               
        def mapType(self):
            # In case of with or without obstacles
            if len(self.map) == 2:
                map = self.map[0]
            else: 
                map = self.map
            return map

        def int2str(self,val1,val2):
            return tuple([val1,val2])

    return [Search(_map_, start, goal, depthLimit).search(), accessable_classes[type].__name__]