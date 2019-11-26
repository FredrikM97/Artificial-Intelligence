import numpy as np
import math
from algorithmSearch.struct import Struct, DFSQueue


class DFS(Struct,DFSQueue):
    def __init__(self):
        super().__init__()
        self.frontier = DFSQueue() 

    def cost_function(self, current):
        return self.getNode(current)['cost'] +1 