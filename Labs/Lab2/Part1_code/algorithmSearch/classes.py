import numpy as np
from random import randint 
import math
from algorithmSearch.struct import Struct, Queue

class BFS(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self, node, current):
        return self.getNode(current)['cost'] +1 

class DFS(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self, node, current):
        return self.getNode(current)['cost'] -1

class Random(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self, node, current):
        return randint(1,100) 

class Greedy_euc(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self,node, current):
        goal = self.goal
        
        return euclides(node,goal)

class Greedy_man(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self,node, current):
        goal = self.goal
        

        return manhattan(node, goal)

class Astar_euc(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue()
         
    def cost_function(self,node, current):
        goal = self.goal
        
        return euclides(node, goal) + self.getNode(current)['g']

class Astar_man(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self,node, current):
        goal = self.goal
        

        return manhattan(node, goal) + self.getNode(current)['g']

class Special(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 
        
    def cost_function(self, node, current):
        goal = self.goal
        
        top = self.map[1][0]
        bottom = self.map[1][1]
        xaxis = self.map[1][2]

        # If robot x is less than middle row, and robot between y axes
        #print(node[1], " and ", node[0])

        if node[1] < xaxis and node[1] > 3 and node[0] < top and node[0] > bottom:
            #print("top:", abs(top - robot.start[0]), " bottom: ", abs(bottom - robot.start[0]))
            if abs(self.start[0]-top) <  abs(self.start[0]-bottom):
                # GO top
                con1 =  (xaxis - abs(node[1] - xaxis))*10 + abs(self.start[0] - top) + manhattan(node, goal)

            else:
                # go bottom
                con1 =  (xaxis-abs(node[1] - xaxis))*10 + abs(self.start[0] - bottom) + manhattan(node, goal)
             

        else:
            con1 =  manhattan(node, goal)
        return con1

def manhattan(node, goal):
    return abs(node[0]-goal[0]) + abs(node[1]-goal[1])


def euclides(node, goal):
    return math.sqrt((node[0]-goal[0])*(node[0]-goal[0]) + (node[1]-goal[1])*(node[1]-goal[1]))