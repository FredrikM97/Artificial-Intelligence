import heapq
from random import randint
class Struct:
    def __init__(self):
        self.parent = [] # No parent
        self.moving_cost = 1 # Each move cost
        self.node = {}

    def addNode(self,parent, node, cost, g):
        if not node in self.node:
            self.createNode(node, parent, cost, g)
        else:
            # Only update parent and cost if new cost is better
            if self.node[node]['cost'] > cost:
                self.node[node]['parent'] = parent
                self.node[node]['cost'] = cost
                self.node[node]['g'] = g
                
    def getNode(self, node):
        if not node in self.node:
            return self.createNode(node)
        else:
            return self.node[node]
    
    def exists(self, node):
        return node in self.node

    def createNode(self,node, parent=0, cost=0, g=0):
        self.node[node] = {
                'parent':parent,
                'cost':cost,
                'g':g
            }
        return self.node[node]

# The biggest value first therefor priority is negative
class Queue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item))

    def remove(self):
        return heapq.heappop(self.elements)[1]
    def printArray(self):
        return self.elements

class BFSQueue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item))
    def remove(self):
        return heapq.heappop(self.elements)[1]
    def printArray(self):
        return self.elements

class DFSQueue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(-1*priority,item))
    def remove(self):
        return heapq.heappop(self.elements)[1]
    def printArray(self):
        return self.elements

class RandomQueue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item))
    def remove(self):
        return self.elements[randint(0, len(self.elements)-1)][1]
    def printArray(self):
        return self.elements
