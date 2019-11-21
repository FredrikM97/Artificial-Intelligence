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
            self.createNode(node)
        else:
            # Only update parent and cost if new cost is better
            if self.node[node][cost] < cost:
                self.node[node][parent] = parent
                self.node[node][cost] = cost
    def getNode(self, node):
        if not node in self.node:
            return self.createNode(node)
        else:
            return self.node[node]

    def createNode(self,node):
        self.node[node] = {
                'parent':0,
                'cost':0
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
    
    # if there is still nodes to open
    while not frontier.isEmpty():
        current = frontier.remove()
        #print("temp ", type(current), "temp2 ", type(robot.goal))
        # check if the goal is reached
        if np.array_equal(current,robot.goal):
            break

        # for each neighbour of the current cell
        # Implement get_neighbors function (return nodes to expand next)
        # (make sure you avoid repetitions!) (if less value -> replace Otherwise dont do anything)
        print("Current parent: ", current)
        
        for next in get_neighbors(list(current),map).items():
            print(next)
            # check if blocked
            if next[1] == -1:
                continue


            # compute cost to reach next cell
            # Implement cost function
            # Get the cost of the parent in order to decide 
            cost = robot.getNode(current)['parent'] +1 #cost_function()
            
            # add next cell to open list
            frontier.add(next, cost)
            # add to path
            robot.addNode(current,next[0], cost) 

    return robot.node

# Do dis
def get_neighbors(current,map):
    # Get the neighbors around
    # If -1 then remember to not check that path
    #dataPoint[[]]
    if len(current) >= 3:
        x = current[0][0]
        y = current[0][1] 
    else:
        x = current[0]
        y = current[1]
    print("dis is current ", len(current), " " , current)
    
    info = {}
    # Get all the items from the four directions
    # Left side
    if x-1 >= 0: 
        info[int2str(x-1,y)] = map[[x-1],[y]][0]
    # Right side
    if x+1 < len(map[0]):
        info[int2str(x+1,y)] = map[[x+1],[y]][0]
    # Top side
    if y+1 < len(map):
        info[int2str(x,y+1)] = map[[x],[y+1]][0]
    # Bottom side
    if y-1 >= 0:
        info[int2str(x,y-1)] = map[[x],[y-1]][0]

    return info

# Do dis
def cost_function():
    pass

def int2str(val1,val2):
    return str(val1)+ ","+str(val2)
    
        