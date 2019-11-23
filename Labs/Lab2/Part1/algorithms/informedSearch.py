import numpy as np
import math
from .informedAlgorithm import Algorithm, Queue

# Map, start pos, goal pos, algType: What kind of cost function 0-3
def search(map, start, goal, algType):
    # cost moving to another cell
    robot = Algorithm(start, goal)
    # open list
    frontier = Queue()



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

            # If object is an obstacle dont add it to the queue
            if obj[1] == -1:
                # Add to path with a value that displays obstacle
                robot.addNode(current,obj[0], -1) 

            else:

                if algType == 0: # Greedy with manhattan distance
                    cost = greedy_man_cost_function(robot, obj[0], current)
                elif algType == 1: # Greedy with euclides distance
                    cost = greedy_euc_cost_function(robot, obj[0], current)
                elif algType == 2: # A* with manhattan distance
                    cost = AStar_man_cost_function(robot, obj[0], current)
                elif algType == 3: # A* with euclides distance
                    cost = AStar_euc_cost_function(robot, obj[0], current)

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

# Greedy search cost -  Manhattan ( |x1 - x2| + |y1 - y2|.)
def greedy_man_cost_function(robot, node, current):
    # Get robot goal position
    # Get Current position
    goal = robot.goal
    pos = node
    #print("Distance: ", abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]))
    return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])

# Greedy search cost -  Euclides (√((x1 - x2)² + (y1 - y2)²))
def greedy_euc_cost_function(robot, node, current):
    # If getting closer increase
    goal = robot.goal
    pos = node
    return math.sqrt((pos[0]-goal[0])*(pos[0]-goal[0]) + (pos[1]-goal[1])*(pos[1]-goal[1]))

# A* search cost function - Manhattan f(x) = g(x) + h(x)
def AStar_man_cost_function(robot, node, current):
    goal = robot.goal
    pos = node
    return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]) + robot.getNode(current)['cost'] + robot.getNode(current)['cost']

# A* search cost function - Manhattan f(x) = g(x) + h(x)
def AStar_euc_cost_function(robot, node, current):
    goal = robot.goal
    pos = node
    return math.sqrt((pos[0]-goal[0])*(pos[0]-goal[0]) + (pos[1]-goal[1])*(pos[1]-goal[1])) + robot.getNode(current)['cost']


def int2str(val1,val2):
    return tuple([val1,val2])
    
def mappedValue(map, x, y):
    return int(map[[x],[y]][0])