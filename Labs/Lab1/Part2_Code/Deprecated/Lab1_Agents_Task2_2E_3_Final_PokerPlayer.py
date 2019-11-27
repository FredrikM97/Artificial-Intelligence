from itertools import product
from random import shuffle
from random import randint
import operator
import re
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from functools import partial
__author__ = 'fyt'

class Agent:
    def __init__(self, hand):
        self.hand = hand
        self.bid = 0
        self.totBid = 0
        self.win = 0
        self.opponentBid = []
        self.opponentCardValue = []
        self.enemyType = "unknown"

################ Stuff to set #######################None
    # Params opponent
    def setBid(self, bid):
        self.setTotalBid(bid)
        self.bid = bid

    def setHand(self,hand):
        self.hand = hand

    # Should be private function
    def setTotalBid(self, bid):
        self.totBid = self.totBid + bid

    def setWinning(self, win):
        self.win = self.win + win
        self.totBid = 0

    def setEnemyType(self, enemy):
        self.enemyType = enemy

    # Remember opponent earlier bets and previous losses
    def addOpponentBid(self, bet):
        self.opponentBid.append(bet)
        
    def addOpponentCards(self, cardValue):
        self.opponentCardValue.append(cardValue)
 

################ Stuff to get #######################   

    def getBid(self):
        return self.bid

    def getTotalBid(self):
        return self.totBid

    def getHand(self):
        return self.hand

    def getWinning(self):
        return self.win

    def getMemory(self):
        return self.opponentBid

    ################ Help functions #######################
    # Check correlation to find out what kind of agent is playing
    def getOpponentType(self):
        
        # Chunk data
        if len(self.opponentBid) >= (3*5) and len(self.opponentBid) % 3 == 0:
            meanValues = list(self.createChunks(self.opponentBid,3))
            #print("Mean value:" + str(meanValues))
            #print("Opponent cards:" + str(self.opponentCardValue))
            corr = np.corrcoef(self.opponentCardValue,meanValues)[1,0]
            # Fixed: Nan Correlation??

            plt.scatter(meanValues, self.opponentCardValue)
            
            if str(corr) == "nan":
                return "fixed"
            # reflex:  high correlation
            elif float(corr) > 0.5:
                return "reflex"
            # Random: Almost 0 correlation
            elif corr < 0.3 and corr > -0.3:
                return "random"
        return "unknown"

    # Create chunks of size n
    def createChunks(self, data, n):
        for i in range(0, len(data), n):
            yield int(np.mean(data[i:i + n]))

################ Agents #######################
class randomAgent(Agent):
    def __init__(self, hand):
        super().__init__(hand)

    # Random bidding
    def bidding(self):
        self.setBid(randint(0,50))

class fixedAgent(Agent):
    def __init__(self, hand):
        super().__init__(hand)
    # Fixed bidding
    def bidding(self, n):
        self.setBid(10*n)

class reflexAgent(Agent):
    def __init__(self, hand):
        super().__init__(hand)
    # Check his own hand
    def bidding(self):
        agentHand = self.getHand().getHandValue()
        self.setBid(round(50*(1-(100/(agentHand+100)))))

class reflexMemAgent(Agent):
    def __init__(self, hand):
        super().__init__(hand)

    # parameters: Opponent agent, check opponents betting
    def bidding(self, agent):
        agentHand = self.getHand().getHandValue()
        opponentBid = self.opponent.getBid()
        self.setBid(round(50*(1-(opponentBid)/(agentHand+opponentBid))))

class reflexMem2Agent(Agent):
    def __init__(self, hand):
        super().__init__(hand)
    # parameters: Opponent agent, Opponent with understanding of opponent
    def bidding(self):
        myHand = self.getHand().getHandValue()
        opponentBid = self.opponent.getBid()
        temp = self.getOpponentType() 

        if temp != "unknown":
            self.enemyType = temp    
        # reflex agent
        if self.enemyType == "reflex":
            self.setBid(round(50*(1-(opponentBid)/(myHand+opponentBid))))
        # Random agent, fixed agent or unknown agent
        else:
            self.setBid(round(50*(1-(100)/(myHand+100))))

################ deck class #######################
class Deck:
    # Construct a deck and shuffle it
    def __init__(self):
        self.suit = ["C","D","H","S"] 
        self.rank = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        self.deck = list(r + s for r, s in product(self.rank, self.suit))
        shuffle(self.deck)

    def getDeck(self):
        return self.deck

class Hand:
    # Create a hand with the size of n
    def __init__(self, deck, n):
        self.hand = deck[:n]
        del deck[-n:], deck[:n]

    # Remove characters from list
    def maskHand(self):
        mask = self.hand
        # Remove all suits
        for i in ['C','D','H','S']:
            mask = [c.replace(i, '') for c in mask]
        # Replace Character ranks with numbers
        for i in ['J','Q','K','A']:
            mask = [c.replace(i, str(['J','Q','K','A'].index(i)+11)) for c in mask]
        # Convert list to integer list
        mask = list(int(s) for s in mask)
        # Sort list
        mask.sort()
        return mask

    # Get value of hand
    def getHandValue(self):
        hand = self.maskHand()
        if(self.check_ThreeOfCards()):
            return hand[0]<<(5*1)
        elif(self.check_Pair()):
            return hand[0]<<(5*2)
        else:
            return self.check_HighCards()

    ################ Check hand value #######################

    def check_HighCards(self):
        return self.hand[2]

    def check_Pair(self):
        return self.hand[0] == self.hand[1] or self.hand[1] == self.hand[2]

    def check_ThreeOfCards(self):
        return self.hand[0] == self.hand[1] and self.hand[0] == self.hand[2] 

# Knows all info on the board
class Board:
    def __init__(self, players):
        self.winPot = 0
        self.boardBids = [players]
        self.deck = Deck()

################ Main loop #######################
class Simulation:
    def __init__(self):
        # Decide agents, agent1 is according to print on last line the smart agent
        #Existing agents: random, fixed, reflex, reflexMem1, reflexMem2
        # Will crash if more so dont change:) (Agent need an update otherwise)
        self.createPlayers([reflexMem2Agent(0), randomAgent(0)]) 
        self.cardAmount = 3 

    def start(self):
        for y in range(50):
            # Start handout of cards
            self.handOut()
            self.bidding()
            
            #Store cards of opponent
            self.agent1.addOpponentCards(self.agent2.getHand().getHandValue())  
        self.showdown()

        print("Winnings: Agent1 {} Agent2 {}".format(self.agent1.getWinning(),self.agent2.getWinning()))
        # Agent1 is the smart agent
        print("Opponent Agent is a: " + str(self.agent1.getOpponentType()) + " Agent")
    def createPlayers(self, agents):
        self.players = [] 
        for i in agents:
            self.players.append(i)
        print(self.players)  

    def handOut(self):
        if self.deck >= len(self.players):
            for i in self.players:
                self.players.setHand(Hand(self.deck, self.cardAmount))
        else:
            print("Not enough cards in deck!")
    def bidding(self):
        # Start bidding phase 0 - 3
        for i in range(1,4):
            # Store bid
            self.agent1.bidding()
            self.agent2.bidding()
            print("Get bidding: " + str(self.agent1.getBid()) + " " + str(self.agent2.getBid()))
            self.winPot = self.agent1.getBid() + self.agent2.getBid()

            #Store bid of opponent
            self.agent1.addOpponentBid(self.agent2.getBid())
            
    def showdown(self):
        agentInfo1 = [self.agent1.getHand().getHandValue, self.agent1.getTotalBid()]
        agentInfo2 = [self.agent2.getHand().getHandValue, self.agent2.getTotalBid()]
        
        # Showdown phase
        if agentInfo1[0] >= agentInfo2[0]):
            self.agent1.setWinning(agentInfo1[1] + agentInfo2[1])
            self.agent2.setWinning((-1*agentInfo2[1]))
            #print("Agent 1 won: ${}".format(agent1.getWinning()))
            
        else:
            self.agent2.setWinning(agentInfo1[1]+ agentInfo2[1])
            self.agent1.setWinning((-1*agentInfo1[1]))
            #print("Agent 2 won: ${}".format(agent2.getWinning()))
simulation = Simulation()
simulation.start()