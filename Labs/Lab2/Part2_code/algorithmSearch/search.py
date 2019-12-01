import numpy as np
from importlib import import_module
from .successor import get_next_states
from random import randint
from .struct import Queue, Struct

class Search(Struct):
    def __init__(self, init_states, type, goal, depthLimit=80):
        super().__init__()
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
            'GREEDY_MANY':-child.nn_current_bidding,    
            'GREEDY_POT':-(child.agent.stack + child.pot),         
            'A*_MANY':self.g - child.nn_current_bidding,
            'A*_POT':self.g - (child.agent.stack + child.pot)      
        }

        return types[self.type]
