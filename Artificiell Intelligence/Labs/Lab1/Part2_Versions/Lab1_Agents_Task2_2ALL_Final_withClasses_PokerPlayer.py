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

class Agent:
    def __init__(self):
        self.hand = []
        self.bid = 0
        self.totBid = 0
        self.balance = 0
        ## Params: bid, cardValue, Type
        self.opponents = {}

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

    def addOpponent(self, players): 
        for opponent in players:
            if opponent == self or opponent in self.opponents:
                continue

            self.opponents[opponent] = {
                'name':opponent.name,
                'type':'unknown',
                'bid':[],
                'cardVal':[]
            }
    def getOpponents(self, opponent):
        if self == opponent:
            return -1
        return self.opponents[opponent]

    ################ Help functions #######################
    # Check correlation to find out what kind of agent is playing
    def getAgentType(self, opponent):
        bid = self.opponents[opponent]['bid']
        cardVal = self.opponents[opponent]['cardVal']

        # Chunk data
        if len(bid) >= (3*5) and len(bid) % 3 == 0 and len(cardVal) > 0:
            meanValues = list(self.createChunks(bid,3))
            corr = np.corrcoef(cardVal,meanValues)[1,0]
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

class reflexMemAgent(Agent):
    def __init__(self):
        super().__init__()

    # Check opponents betting (dont handle multiple opponents)
    def bidding(self, board):
        agentHand = self.hand.getHandValue()
        for player in board.game.players:
            opponentBid = player.bid
        self.setBid(round(50*(1-(opponentBid)/(agentHand+opponentBid))))
        return self.bid

class reflexMem2Agent(Agent):
    def __init__(self):
        super().__init__()
    # parameters: Opponent agent, Opponent with understanding of opponent
    def bidding(self, board):
        
        myHand = self.hand.getHandValue()
        
        # Just assume that there is only one other player :)
        # If no other have bid
        if len(board.boardBids) == 0:
            opponentBid = 100
        else:
            for player in board.boardBids.keys():
                if player == self:
                    continue
                opponentBid = board.boardBids[player]
                
        oldBid = 0
        newBid = 0
        for player in board.game.players:
            if player == self:
                continue
            
            temp = self.getAgentType(player) 
            
            if temp != "unknown":
                self.opponents[player]['type'] = temp    
            # reflex agent
            if temp == "reflex":
                #self.setBid(round(50*(1-(opponentBid)/(myHand+opponentBid))))
                newBid = round(50*(1-(opponentBid)/(myHand+opponentBid)))
            # Random agent, fixed agent or unknown agent
            else:
                #self.setBid(round(50*(1-(100)/(myHand+100))))
                newBid = round(50*(1-(100)/(myHand+100)))
            if newBid <= oldBid:
                oldBid = newBid
                self.setBid(oldBid)
        return self.bid


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
        return max(Counter(hand))<<(5*max(Counter(hand).values()))
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
                player.setHand(Hand(self.deck, cardAmount))
        else:
            return -1

    # Only memorise bit of one Round!
    def bid(self):
        self.round = self.round + 1
        for player in self.game.players:
            self.boardBids[player] = player.bidding(self)
            player.addBalance((-1*player.bid))  
            self.sumWinPot(player.bid)

        for player1 in self.game.players:
            for player2 in self.game.players:
                if player1 == player2:
                    continue
                player1.opponents[player2]['bid'].append(self.boardBids[player2])
        return self

    def addPlayerHands(self):
        for player in self.game.players:
            self.playerHands[player] = player.hand.getHandValue()

    def sumWinPot(self, bid):
        self.winPot = self.winPot + bid

    def addPlayerHand(self, player):
        self.playerHands[player] = player.getHandValue()

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
            self.showdown(board)
        
        return self
            
    def createPlayer(self, players): # Done
        for player in players:
            player[1].name = player[0]
            self.players.append(player[1])

        for player in self.players:
            player.addOpponent(self.players)

        return self

    def showdown(self, board):    
        # Add each players hand to the board player  hand
        board.addPlayerHands()

        # Store opponents cardVals in each agent
        for player1 in self.players:
            for player2 in self.players:
                if player1 == player2:
                    continue
                player1.opponents[player2]['cardVal'].append(board.playerHands[player2])                 
        # Showdown phase - Get winner
        winner = sorted(board.playerHands.items(), key=lambda x: x[1])[-1][0]
        for player in self.players:
            if player == winner:
                player.addBalance(board.winPot)
        
# How many games and which agent to plot
def run_plot(games,agent):
    agentScore = []
    for x in range(0,games):
        game = run(games)
        agentScore.append([p.balance for p in game.players][agent])
        printFinal(game)
    #createPlot(agentScore)
    

def run(games):
        # Min 8 rounds to know the other agents
        game = Simulation(3)
        game.createPlayer([["Johnny", reflexMem2Agent()], ["Burp",randomAgent()], ["Na", fixedAgent()]])
        return game.start()

def printFinal(game):
    # Print final
    for player in game.players:
        print("\n" + player.name + ":")
        for opponent in player.opponents.values():
            getType = str(opponent['type'])
            print(opponent['name'] +  " is: " + getType + " Agent")
        print("Balance: " + str(player.balance))

def createPlot(data):
        counts, bins = np.histogram(data)
        plt.hist(bins[:-1], bins, weights=counts)

        plt.legend(['Agent 0'])
        plt.xlabel('Winnings')
        plt.ylabel('Occurrence')
        plt.show()

if __name__ == "__main__":
    #game.createPlayer(fixedAgent(), "Becky")
    run_plot(1,0)
    