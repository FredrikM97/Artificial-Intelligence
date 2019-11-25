import heapq
from random import randint
class Algorithm:
    def __init__(self, map, start, goal):
        self.parent = [] # No parent
        self.start = start # Start position
        self.goal = goal # TO search for
        self.moving_cost = 1 # Each move cost
        self.node = {}
        self.map = map

    def addNode(self,parent, node, cost):
        if not node in self.node:
            self.createNode(node, parent, cost)
        else:
            # Only update parent and cost if new cost is better
            if self.node[node]['cost'] > cost:
                self.node[node]['parent'] = parent
                self.node[node]['cost'] = cost
                
    def getNode(self, node):
        if not node in self.node:
            return self.createNode(node, 0, 0)
        else:
            return self.node[node]

    def exists(self, node):
        return node in self.node

    def createNode(self,node, parent, cost):
        self.node[node] = {
                'parent':parent,
                'cost':cost
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

