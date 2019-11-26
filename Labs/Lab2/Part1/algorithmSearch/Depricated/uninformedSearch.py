import numpy as np
from .uninformedAlgorithm import Algorithm, BFSQueue, DFSQueue, RandomQueue

# Map, start pos, goal pos, Search Type [0: BFS, 1: DFS, 2: Random]
def search(map, start, goal, searchType):
    # cost moving to another cell
    robot = Algorithm(start, goal)
    # open list
    if searchType == 0:
        frontier = BFSQueue()
    elif searchType == 1:
        frontier = DFSQueue()
    elif searchType == 2:
        frontier = RandomQueue()



    # add starting cell to open list
    frontier.add(start,0)

    # add to path
    robot.addNode(None,start, 0) 
    
    # if there is still nodes to open
    while not frontier.isEmpty():
        current = frontier.remove()
        # check if the goal is reached
        if np.array_equal(current,robot.goal):
            print("Found the goal!!")
            break

        # for each neighbour of the current cell
        # Implement get_neighbors function (return nodes to expand next)
        # (make sure you avoid repetitions!) (if less value -> replace Otherwise dont do anything)

        for obj in get_neighbors(list(current),map).items():   

            # If object is an obstacle dont add it to the queue
            if obj[1] == -1:
                # Add to path with a value that displays obstacle
                robot.addNode(current,obj[0], -1) 

            else:

                cost = cost_function(robot, current)
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
            info[pos] = int(map[[pos[0]],[pos[1]]][0])

    return info

# Do dis
def cost_function(robot, current):
    return robot.getNode(current)['cost'] +1 

def int2str(val1,val2):
    return tuple([val1,val2])
    
