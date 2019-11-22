import numpy as np
import math
import heapq

class Queue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(-1*priority,item))
    def remove(self):
        return heapq.heappop(self.elements)[1]
    def printArray(self):
        return self.elements

class dfs:
    def __init__(self,start, goal):
        self.parent = [] # No parent
        self.g = 0 #Total path cost
        self.start = start # Start position
        self.goal = goal # TO search for
        self.moving_cost = 1 # Each move cost
        self.node = {}

    def addNode(self,parent, node, cost):
        if not node in self.node:
            self.createNode(node, parent, cost)
        else:
            # Only update parent and cost if new cost is better
            if self.node[node]['cost'] > cost:
                self.node[node]['parent'] = parent
                self.node[node]['cost'] = cost
                
    def getNode(self, node):
        if not node in self.node:
            return self.createNode(node, 0, 0)
        else:
            return self.node[node]

    def exists(self, node):
        return node in self.node

    def createNode(self,node, parent, cost):
        self.node[node] = {
                'parent':parent,
                'cost':cost
            }
        return self.node[node]


# An example of search algorithm
# modify it and implment the missing part
def search(map, start, goal):
    # cost moving to another cell
    robot = dfs(start, goal)
    # open list

    frontier = Queue() # Remember steps
    # add starting cell to open list
    frontier.add(start,0)
    # if there is still nodes to open
    while not frontier.isEmpty():
        current = frontier.remove()
        # check if the goal is reached
        if np.array_equal(current,robot.goal):
            print("Found the goal!!")
            print(frontier.printArray())
            break

        # for each neighbour of the current cell
        # Implement get_neighbors function (return nodes to expand next)
        # (make sure you avoid repetitions!) (if less value -> replace Otherwise dont do anything)

        for obj in get_neighbors(list(current),map).items():

            # check if blocked
            if obj[1] == -1:
                continue
            cost = robot.getNode(current)['cost'] +1
            
            # add next cell to open list
            if not robot.exists(obj[0]):
                frontier.add(obj[0], cost)

            # add to path
            robot.addNode(current,obj[0], cost) 

    return robot.node

# Do dis
def get_neighbors(current,map):
    # Get the neighbors around
    x = current[0]
    y = current[1]
    
    
    info = {}
    # Get all the items from the four directions
    paths = [(x-1,y), (x+1,y),(x,y+1), (x,y-1)]
    maplen = len(map)
    
    for pos in paths:
        con1 = pos[0] >= 0 and pos[1] >= 0
        con2 = pos[0] < maplen and pos[1] < maplen
        if  con1 and con2:
            info[pos] = mappedValue(map, pos[0],pos[1])

    return info

# Do dis
def cost_function(current):
    pass 

def int2str(val1,val2):
    return tuple([val1,val2])
    
def mappedValue(map, x, y):
    return int(map[[x],[y]][0])
    
        