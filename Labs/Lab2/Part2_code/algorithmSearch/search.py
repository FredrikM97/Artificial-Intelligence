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
    def __init__(self, init_states, type, goal,strategy, depthLimit=80):
        super().__init__()
        self.strategy = strategy
        self.initStates = init_states
        self.goal = goal # TO search for
        self.steps = 0
        self.depthLimit = depthLimit
        self.type = type
        self.frontier = Queue()
        self.frontier.add(self.initStates,0)
        self.addNode(None,self.initStates, 0, 0)
        

    def search(self):
        # if there is still nodes to open
        while not self.frontier.isEmpty():
            current = self.frontier.remove()
            self.steps += 1
    
            # Goal reached if differance between agent and opponent is 100
            winnings = (current.agent.stack - current.opponent.stack)/2
            if winnings >= self.goal:
                self.g = self.node[current]['g']
                return self
            
            # If Maximum depth is reached skip state
            if self.node[current]['g'] > self.depthLimit or current.nn_current_hand >= 4:
                continue
            

            if self.type == "RANDOM" and self.steps > 10000:
                break

            # Start checking each node
            for obj in self.get_neighbors(current): 

                self.g = self.node[current]['g'] + 1
                cost = self.getAlgorithmType(obj)

                # add next cell to open list
                if not self.exists(obj):
                    self.frontier.add(obj, cost)
                
                # add to path
                self.addNode(current,obj, cost, self.g) 

        return -1
        
    # Custom heuristics (bonus part), default: many
    # Manhattan and euclides is NOT implemented for the poker game - Added for future use
    def get_heuristic(self,child):
        strategy = {
            'MANY':-child.nn_current_bidding,
            'BIG':-(child.agent.stack + child.pot) ## Get the big pot
            #'MANHATTAN':(abs(child[0]-self.goal[0]) + abs(child[1]-self.goal[1])), 
            #'EUCLIDES':(((child[0]-self.goal[0])**2 + (child[1]-self.goal[1])**2)**(1/2))
        }
        if not self.strategy in strategy: return strategy['MANY']
        return strategy[self.strategy]
        

    def get_neighbors(self, parent):
        # Init state
        if self.steps == 0:
            info = get_next_states(self.initStates)
        else:
            info = get_next_states(parent)
        return info

    # Differen algorithms
    def getAlgorithmType(self, child):
        types = {
            'BFS':self.g,               
            'DFS':-self.g,              
            'RANDOM':randint(1,100),    
            'GREEDY':self.get_heuristic(child),            
            'A*':self.g + self.get_heuristic(child)              
        }

        return types[self.type]
