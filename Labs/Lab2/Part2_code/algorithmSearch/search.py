import numpy as np
from importlib import import_module
from .successor import get_next_states
from random import randint
from .struct import Queue, Struct

class heuristic:
    def __init__(self):
        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = 0

class Search(Struct):
    def __init__(self, init_states, type, goal,heuristic='big', depthLimit=-1):
        super().__init__()
        self.heuristic = heuristic
        self.initStates = init_states
        self.goal = goal # TO search for
        self.steps = 0
        self.depthLimit = depthLimit
        self.type = type
        self.frontier = Queue()
        self.frontier.add(self.initStates,0)
        self.addNode(None,self.initStates, 0, 0)
        

    def search(self):
        start = heuristic()
        # if there is still nodes to open
        while not self.frontier.isEmpty():
            current = self.frontier.remove()
            self.steps += 1
    
            # Goal reached if differance between agent and opponent is 100
            winnings = (current.agent.stack - current.opponent.stack)/2
            if winnings >= self.goal:
                self.g = self.node[current]['g']
                break
            
            # If Maximum depth is reached skip state
            if not self.depthLimit == -1 and self.depthLimit <= self.node[current]['g'] or current.nn_current_hand >= 4:
                continue
            

            # Start checking each node
            for obj in self.get_neighbors(current):   
                #cost = self.cost_function(obj, current)
                
                start.g = self.node[current]['g'] + 1
                start.h = self.get_heuristic(obj)
                start.f = start.g + start.h
                start.cost = self.getAlgorithmType(start)

                # add next cell to open list
                if not self.exists(obj):
                    self.frontier.add(obj, start.cost)

                # add to path
                self.addNode(current,obj, start.cost, start.g) 

        return self
        
    # Added in order to decide if we want big pots or many bets
    def get_heuristic(self,obj):
        if self.heuristic == "big": ## Get the big pot
            return -(obj.agent.stack + obj.pot)
        return -obj.nn_current_bidding ## Get many biddings

    def get_neighbors(self, current):
        # Init state
        if self.steps == 0:
            info = get_next_states(self.initStates)
        else:
            info = get_next_states(current)
        return info

    def getAlgorithmType(self, cost):
        types = {
            'BFS':cost.g,               #BFS
            'DFS':-cost.g,              #DFS
            'RANDOM':randint(0,100),    #Random
            'GREEDY':cost.h,            #Greedy
            'A*':cost.f                 #A*
        }
        return types[self.type]
