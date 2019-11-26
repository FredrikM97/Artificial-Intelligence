import numpy as np
from algorithms.smartSearch import SmartSearch
from algorithms.informedSearch import informedSearch
class Search(SmartSearch):
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
                
            return self.node

    def int2str(self,val1,val2):
        return tuple([val1,val2])

    def calculatePathCost(self):
        g = 0
        node = self.getNode(self.goal)
        while node['cost'] != 0:
            g += 1
            node = self.getNode(node['parent'])

        return g