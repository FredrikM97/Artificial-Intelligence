import numpy as np
import math
from algorithmSearch.struct import Struct, BFSQueue, RandomQueue, DFSQueue, Queue

class BFS(Struct,BFSQueue):
    def __init__(self):
        super().__init__()
        self.frontier = BFSQueue() 

    def cost_function(self, node, current):
        return self.getNode(current)['cost'] +1 

class DFS(Struct,DFSQueue):
    def __init__(self):
        super().__init__()
        self.frontier = DFSQueue() 

    def cost_function(self, node, current):
        return self.getNode(current)['cost'] +1 

class Random(Struct,RandomQueue):
    def __init__(self):
        super().__init__()
        self.frontier = RandomQueue() 

    def cost_function(self, node, current):
        return self.getNode(current)['cost'] +1 

class Greedy_euc(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    # greedy_euc_cost_function
    def cost_function(self,node, current):
        goal = self.goal
        pos = node
        return math.sqrt((pos[0]-goal[0])*(pos[0]-goal[0]) + (pos[1]-goal[1])*(pos[1]-goal[1])) +1

class Greedy_man(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    # greedy_man_cost_function
    def cost_function(self,node, current):
        goal = self.goal
        pos = node

        return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])



class Astar_euc(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue()
         
    # AStar_euc_cost_function
    def cost_function(self,node, current):
        goal = self.goal
        pos = node

        return math.sqrt((pos[0]-goal[0])*(pos[0]-goal[0]) + (pos[1]-goal[1])*(pos[1]-goal[1])) + self.getNode(current)['cost']

class Astar_man(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    # AStar_man_cost_function
    def cost_function(self,node, current):
        goal = self.goal
        pos = node

        return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]) + self.getNode(current)['cost']

class Special(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 
        
    def cost_function(self, node, current):
        goal = self.goal
        pos = node
        top = self.map[1][0]
        bottom = self.map[1][1]
        xaxis = self.map[1][2]

        # If robot x is less than middle row, and robot between y axes
        #print(pos[1], " and ", pos[0])

        if pos[1] < xaxis and pos[1] > 3 and pos[0] < top and pos[0] > bottom:
            #print("top:", abs(top - robot.start[0]), " bottom: ", abs(bottom - robot.start[0]))
            if abs(self.start[0]-top) <  abs(self.start[0]-bottom):
                # GO top
                con1 =  (xaxis - abs(pos[1] - xaxis))*10 + abs(self.start[0] - top) +abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])
                #print('Going top')
            else:
                # go bottom
                con1 =  (xaxis-abs(pos[1] - xaxis))*10 + abs(self.start[0] - bottom) + abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])
                #print('Going bot')

        else:
            con1 =  abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])
        return con1