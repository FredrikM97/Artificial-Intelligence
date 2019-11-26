import numpy as np
import math
from algorithmSearch.struct import Struct, RandomQueue


class Random(Struct,RandomQueue):
    def __init__(self):
        super().__init__()
        self.frontier = RandomQueue() 

    def cost_function(self, current):
        return self.getNode(current)['cost'] +1 