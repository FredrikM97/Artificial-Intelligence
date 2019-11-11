from itertools import product
from random import shuffle
from random import randint
#import operator
#import re
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from functools import partial
from collections import Counter

np.seterr(divide='ignore', invalid='ignore')
__author__ = 'fyt'

class Observer:
    def update(self, board):
        pass
    def getAgents(self, game):
        pass
class Agent:
    def __init__(self):
        self.hand = []
        self.bid = 0
        self.totBid = 0
        self.balance = 0
        

################ Stuff to set #######################None
    # Params opponent
    def setBid(self, bid):
        self.setTotalBid(bid)
        self.bid = bid

    def setHand(self,hand):
        self.hand = hand

    # Should be private function
    def setTotalBid(self, bid):
        self.totBid += bid

    def addBalance(self, balance):
        self.balance += balance
        self.totBid = 0

################ Agents #######################
class randomAgent(Agent):
    def __init__(self):
        super().__init__()

    # Random bidding
    def bidding(self, board):
        self.setBid(randint(0,50))
        return self.bid

class fixedAgent(Agent):
    def __init__(self):
        super().__init__()
    # Fixed bidding
    def bidding(self, board):
        self.setBid(5 + 10*board.round)
        return self.bid

class reflexAgent(Agent):
    def __init__(self):
        super().__init__()
    # Check his own hand
    def bidding(self, board):
        agentHand = self.hand.getHandValue()
        self.setBid(round(50*(1-(100/(agentHand+100)))))
        return self.bid

class reflexMemAgent(Agent,Observer):
    def __init__(self):
        super().__init__()
        ## Params: bid, cardValue, Type
        self.opponents = {}
    
    def update(self,board):
        for key in board.playerHands.keys():
            if key == self: continue
            self.addOpponent(key)
            self.opponents[key]['cardVal'].append(board.playerHands[key])
            self.opponents[key]['bid'].extend(board.boardBids[key]) 

    def getAgents(self):
        print("Balance: " + str(self.balance))

    # Check opponents betting (dont handle multiple opponents)
    def bidding(self, board):
        myHand = self.hand.getHandValue()

        oldBid = 50
        newBid = 0
        for player in board.game.players:
            if player == self:
                continue
            opponentBid = player.bid

            newBid = round(50*(1-(opponentBid)/(myHand+opponentBid)))

            if newBid <= oldBid:
                    oldBid = newBid
                    self.setBid(oldBid)
        return self.bid

    def addOpponent(self, player): 
        if player in self.opponents:
            return -1

        self.opponents[player] = {
            'name':player.name,
            'type':'unknown',
            'bid':[],
            'cardVal':[]
        }
        return 0
class reflexMem2Agent(Agent,Observer):
    def __init__(self):
        super().__init__()
        ## Params: bid, cardValue, Type
        self.opponents = {}
    
    def update(self,board):
        for key in board.playerHands.keys():
            if key == self: continue
            self.addOpponent(key)
            self.opponents[key]['cardVal'].append(board.playerHands[key])
            self.opponents[key]['bid'].extend(board.boardBids[key]) 

    def getAgents(self):
        for player in self.opponents:
            print(self.opponents[player]['name'] +  " is: " + self.opponents[player]['type'] + " Agent")
        print("Balance: " + str(self.balance))

    def addOpponent(self, player): 
        if player == self or player in self.opponents:
            return -1

        self.opponents[player] = {
            'name':player.name,
            'type':'unknown',
            'bid':[],
            'cardVal':[]
        }
        return 0

    # parameters: Opponent agent, Opponent with understanding of opponent
    def bidding(self, board):
        
        myHand = self.hand.getHandValue()
        oldBid = 50
        newBid = 0
        for player in self.opponents:
            if player == self:
                continue

            # Get type
            temp = self.getAgentType(player)
            # In case that bids on the board could be empty
            if len(board.boardBids[player]) == 0:
                opponentBid = 100
            else:
                opponentBid = board.boardBids[player][-1:][0]
            if temp != "unknown":
                self.opponents[player]['type'] = temp    
            # reflex agent
            if temp == "reflex":
                newBid = round(50*(1-(opponentBid)/(myHand+opponentBid)))
            # Random agent, fixed agent or unknown agent
            else:
                newBid = round(50*(1-(100)/(myHand+100)))
                # TODO
            if newBid <= oldBid:
                oldBid = newBid
                self.setBid(oldBid)

        return self.bid

    # Check correlation to find out what kind of agent is playing
    def getAgentType(self, opponent):
        bid = self.opponents[opponent]['bid']
        cardVal = self.opponents[opponent]['cardVal']
        
        # Chunk data
        if len(bid) > 3*2 and len(bid) % 3 == 0 and len(cardVal) > 0:
            #print("derp " + str(bid) + " and " + str(cardVal))
            meanValues = list(self.createChunks(bid,3))
            corr = np.corrcoef(cardVal,meanValues)[1,0]

            #print(str(corr) + " sec " + str(meanValues) + " third " +  str(list(self.createChunks(bid,3))))
            if str(corr) == "nan":
                return "fixed"
            # reflex:  high correlation
            elif float(corr) > 0.5:
                return "reflex"
            # Random: Almost 0 correlationopponent
            elif corr < 0.3 and corr > -0.3:
                return "random"
        return "unknown"

    # Create chunks of size n
    def createChunks(self, data, n):
        for i in range(0, len(data), n):
            yield int(np.mean(data[i:i + n]))
    


################ deck class #######################
class Deck:
    # Construct a deck and shuffle it
    def __init__(self):
        self.suit = ["C","D","H","S"] 
        self.rank = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
        self.deck = list(s + r for (s, r) in product(self.suit, self.rank))
        shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def drawCards(self, n):
        hand = self.deck[:n]
        del self.deck[-n:], self.deck[:n]
        return hand

class Hand:
    # Create a hand with the size of n
    def __init__(self, deck, n):
        self.deck = Deck()
        self.hand = deck.drawCards(n)

    # Remove characters from list
    def maskHand(self):
        mask = [list(c)[1] for c in self.hand]
        dic = {key: val +2 for val, key in enumerate(self.deck.rank)}
        return sorted([dic[s] for s in mask], reverse=True)


    # Get value of hand
    def getHandValue(self):
        hand = self.maskHand()
        return max(Counter(hand))<<(5*(max(Counter(hand).values())-1))
# Knows all info on the board
class Board:
    def __init__(self, game):
        self.winPot = 0
        self.boardBids = {}
        self.playerHands = {}
        self.deck = Deck()
        self.game = game
        self.round = 0

    def __len__(self):
        return len(self.boardBids)

    def handOut(self, cardAmount): # Done
        if len(self.deck) >= (len(self.game.players)*cardAmount):
            for player in self.game.players:
                self.boardBids[player] = []
                player.setHand(Hand(self.deck, cardAmount))
        else:
            return -1

        return self
        
    # Only memorise bit of one Round!
    def bid(self):
        self.round = self.round + 1
        for player in self.game.players:
            self.boardBids[player].append(player.bidding(self))
            player.addBalance((-1*player.bid))  
            self.sumWinPot(player.bid)
        return self

    def showdown(self):    
        # Add each players hand to the board player  hand
        for player in self.game.players:
            self.playerHands[player] = player.hand.getHandValue()

        for player in self.game.players:
            if issubclass(player.__class__, Observer): 
                player.update(self)

        # Showdown phase - Get winner
        winner = sorted(self.playerHands.items(), key=lambda x: x[1])[-1][0]
        for player in self.game.players:
            if player == winner:
                player.addBalance(self.winPot)

        return self

    def sumWinPot(self, bid):
        self.winPot = self.winPot + bid

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
        game.createPlayer([["Johnny",reflexMem2Agent()], ["Burp",reflexMemAgent()], ["Bab",randomAgent()]]) 
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
    