import numpy as np
import math
from algorithmSearch.struct import Struct, BFSQueue


class BFS(Struct,BFSQueue):
    def __init__(self):
        super().__init__()
        self.frontier = BFSQueue() 

    def cost_function(self, current):
        return self.getNode(current)['cost'] +1 