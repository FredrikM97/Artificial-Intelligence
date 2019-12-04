import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from functools import partial

from agents.reflexMem2 import reflexMem2Agent
from agents.random import randomAgent
from game.board import Board
from game.observer import Observer

np.seterr(divide='ignore', invalid='ignore')
__author__ = 'fyt'

################ Main loop #######################
class Simulation:
    def __init__(self, rounds=50):
        # Max two agents, choose between agents in Agent class
        self.players = [] 
        self.cardAmount = 3 
        self.rounds = rounds
        
    def start(self):
        for x in range(0,self.rounds):
            # Create clean board
            board = Board(self)

            # Deal cards
            if board.handOut(self.cardAmount) == -1: return -1

            # Start bidding phase 0 - 3
            board.bid().bid().bid()

            # Showdown
            board.showdown()
        return self
            
    def createPlayer(self, players): # Done
        for player in players:
            player[1].name = player[0]
            self.players.append(player[1])

        
        return self
        
# How many games and which agent to plot
def run_plot(games,agent):
    agentScore = []
    for x in range(0,games):
        game = run(games)
        agentScore.append([p.balance for p in game.players][agent])
    createPlot(agentScore)
    

def run(games):
        # Min 8 rounds to know the other agents
        game = Simulation(6)
        game.createPlayer([["Johnny",reflexMem2Agent()], ["Burp",reflexMem2Agent()], ["Bab",randomAgent()]]) 
        #, ["Na", fixedAgent()]
        game.start()
        printFinal(game)
        return game

def printFinal(game):
    # Print final
    
    for player in game.players:
        print("\n" + str(player.name) + ":")
        if issubclass(player.__class__, Observer): player.getAgents()
        else: print("Balance: " + str(player.balance) )

def createPlot(data):
        counts, bins = np.histogram(data)
        plt.hist(bins[:-1], bins, weights=counts)

        plt.legend(['Agent 0'])
        plt.xlabel('Winnings')
        plt.ylabel('Occurrence')
        plt.show()

if __name__ == "__main__":
    #game.createPlayer(fixedAgent(), "Becky")
    run(1)
    #run_plot(1,0)
    
