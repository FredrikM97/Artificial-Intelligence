import numpy as np
import math
from algorithms.struct import Struct, Queue


class SmartSearch(Struct,Queue):
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

        if pos[1] < xaxis and pos[0] < top and pos[0] > bottom:
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