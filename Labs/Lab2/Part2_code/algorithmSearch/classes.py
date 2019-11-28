import numpy as np
import math
from algorithmSearch.struct import Struct, RandomQueue, Queue

class BFS(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self, node, current):
        return self.getNode(current)['g'] +1

class DFS(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    def cost_function(self, node, current):
        return -self.getNode(current)['g'] +1

class Random(Struct,RandomQueue):
    def __init__(self):
        super().__init__()
        self.frontier = RandomQueue() 

    def cost_function(self, node, current):
        return self.getNode(current)['g'] +1

class Greedy(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    # greedy_euc_cost_function
    def cost_function(self,node, current):
        return self.get_heuristic(node)

class Astar(Struct,Queue):
    def __init__(self):
        super().__init__()
        self.frontier = Queue() 

    # AStar_man_cost_function
    def cost_function(self,node, current):
        return self.get_heuristic(node) + self.getNode(current)['g'] +1
