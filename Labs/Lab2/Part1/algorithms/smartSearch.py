import numpy as np
import math
from .informedAlgorithm import Algorithm, Queue

# Map, start pos, goal pos
def search(map, start, goal):
    # cost moving to another cell
    robot = Algorithm(map, start, goal)
    # open list
    frontier = Queue()
    startPosition = 'None'

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

        for obj in get_neighbors(list(current),map[0]).items():   

            # If object is an obstacle dont add it to the queue
            if obj[1] == -1:
                continue

            else:

               
                cost = SmartSearchT_cost_function(robot,obj[0], current,startPosition)

                # add next cell to open list
                if not robot.exists(obj[0]):
                    frontier.add(obj[0], cost)

                # add to path
                robot.addNode(current,obj[0], cost) 

    return robot.node

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

def int2str(val1,val2):
    return tuple([val1,val2])

def SmartSearchT_cost_function(robot, node, current,startPosition):
    goal = robot.goal
    pos = node
    top = robot.map[1][1]
    bottom = robot.map[1][1]
    xaxis = robot.map[1][2]


   
    if startPosition == 'None':
        if robot.start[0] > 30:
            con1 = abs(60 - pos[0])*10
        elif robot.start[0] <= 30:
            con1 = abs(0 - pos[0])*10

        if con1 < 2:
            startPosition = 'straight'

    if startPosition == 'straight':
        con1 = abs(60-pos[1])*10

        if con1 < 2:
            startPosition = 'search'
    print(con1)
    if startPosition == 'search':
    # distance: goal and pos + middle 
        con1 = abs(pos[1]-goal[1]) + abs(pos[0]-goal[0]) + 

    # If x

    return con1
    
   