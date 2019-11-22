import numpy as np
import math
import heapq

class Queue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item))
    def remove(self):
        return heapq.heappop(self.elements)[1]
    def printArray(self):
        return self.elements

class bfs:
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
        #print("Creating node: ", node," Parent: ", parent)
        self.node[node] = {
                'parent':parent,
                'cost':cost
            }
        return self.node[node]



# An example of search algorithm
# modify it and implment the missing part
def search(map, start, goal):
    # cost moving to another cell
    robot = bfs(start, goal)
    # open list

    frontier = Queue() # Remember steps
    # add starting cell to open list
    frontier.add(start,0)
    #print("Frontier array after add: ", frontier.printArray())

    # if there is still nodes to open
    while not frontier.isEmpty():
        current = frontier.remove()
        #print("temp ", type(current), "temp2 ", type(robot.goal))
        # check if the goal is reached
        if np.array_equal(current,robot.goal):
            print("Found the goal!!")
            break

        # for each neighbour of the current cell
        # Implement get_neighbors function (return nodes to expand next)
        # (make sure you avoid repetitions!) (if less value -> replace Otherwise dont do anything)
        #print("Frontier array after add: ", frontier.printArray())
        #print("Visited nodes: ", robot.node )
        #print("Get Parent: ", robot.getNode(current))
        #print("Current parent: ", current)
        
        for val in get_neighbors(list(current),map).items():
            nextKey = val[0]
            nextObj = val[1]

            #print("Next key: ",nextKey, "NextObj: ", nextObj)
            # check if blocked
            if nextObj == -1:
                continue


            # compute cost to reach next cell
            # Implement cost function
            # Get the cost of the parent in order to decide 
            
            cost = robot.getNode(current)['cost'] +1 #cost_function()
            
            # add next cell to open list
            if not robot.exists(nextKey):
                frontier.add(nextKey, cost)

            # add to path
            robot.addNode(current,nextKey, cost) 

    return robot.node

# Do dis
def get_neighbors(current,map):
    # Get the neighbors around
    # If -1 then remember to not check that path
    #dataPoint[[]]
    #print("Length of current ", len(current), "  Data in current: " , current)
    x = current[0]
    y = current[1]
    
    
    info = {}
    # Get all the items from the four directions
    # Left side
    '''
    if x-1 >= 0: 
        info[int2str(x-1,y)] = mappedValue(map,x-1,y)
    # Right side
    if x+1 < len(map[0]):
        info[int2str(x+1,y)] = mappedValue(map,x+1,y)
    # Top side
    if y+1 < len(map):
        info[int2str(x,y+1)] = mappedValue(map, x,y+1)
    # Bottom side
    if y-1 >= 0:
        info[int2str(x,y-1)] = mappedValue(map, x,y-1)
    '''
    paths = [(x-1,y), (x+1,y),(x,y+1), (x,y-1)]
    maplen = len(map)
    
    for pos in paths:
        con1 = pos[0] >= 0 and pos[1] >= 0
        con2 = pos[0] < maplen and pos[1] < maplen
        if  con1 and con2:
            info[pos] = mappedValue(map, pos[0],pos[1])

    #print("Current data in info: ", info)
    return info

# Do dis
def cost_function():
    pass

def int2str(val1,val2):
    return tuple([val1,val2])
    
def mappedValue(map, x, y):
    return int(map[[x],[y]][0])
    
        