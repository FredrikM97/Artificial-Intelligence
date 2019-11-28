
import numpy as np
import math
from algorithmSearch.struct import Struct, Queue

class Greedy_man(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    # greedy_man_cost_function
    def cost_function(self,node, current):
        goal = self.goal
        pos = node

        return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]) +1