from itertools import product
from random import shuffle
from random import randint
import operator
import re
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
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

################ Stuff to set #######################
    def setBid(self, bid):
        self.setTotalBid(bid)
        self.bid = bid

    def setHand(self,hand):
        if len(deck) > 3:
            self.hand = hand
        else:
            print("Not enough cards in deck")

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

################ Agents #######################

    # Random bidding
    def randomAgent(self):
        return randint(0,50)

    # Fixed bidding
    def fixedAgent(self,n):
        return 10*n

    # Check his own hand
    def reflexAgent(self):
        agentHand = getHandValue(self.getHand())
        return round(50*(1-(100/(agentHand+100))))

    # parameters: Opponent agent, check opponents betting
    def reflexMemAgent(self, agent):
        agentHand = getHandValue(self.getHand())
        opponentBid = agent.getBid()
        return round(50*(1-(opponentBid)/(agentHand+opponentBid)))

    # parameters: Opponent agent, Opponent with understanding of opponent
    def reflexMem2Agent(self, agent):
        agentHand = getHandValue(self.getHand())
        opponentBid = agent.getBid()

        temp = self.getEnemyType() 
        if temp != "unknown":
            self.enemyType = temp
            
        # Reflex agent
        if self.enemyType == "reflex":
            return round(50*(1-(opponentBid)/(agentHand+opponentBid)))
        # Random agent, fixed agent or unknown agent
        else:
            return round(50*(1-(100)/(agentHand+100)))

################ Help functions #######################
    # Check correlation to find out what kind of agent is playing
    def getEnemyType(self):
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
            # Reflex:  high correlation
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

################ Construct deck #######################

# Construct a deck and shuffle it
def constructDeck():
    suit = ["C","D","H","S"] 
    rank = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    deck = list(r + s for r, s in product(rank, suit))
    shuffle(deck)
    return deck

################ hand Actions #######################

# Return a hand with the size of n
def createHand(n):
    newHand = deck[:n]
    del deck[-n:], deck[:n]
    return newHand

# Remove characters from list
def maskHand(mask):
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
def getHandValue(agent):
    mask = maskHand(agent)
    if(check_ThreeOfCards(mask)):
        return mask[0]<<(5*1)
    elif(check_Pair(mask)):
        return mask[0]<<(5*2)
    else:
        return check_HighCards(mask)

################ Check hand value #######################

def check_HighCards(hand):
    return hand[2]

def check_Pair(hand):
    return hand[0] == hand[1] or hand[1] == hand[2]

def check_ThreeOfCards(hand):
    return hand[0] == hand[1] and hand[0] == hand[2] 


################ Main loop #######################


deck = constructDeck()
agent1 = Agent(createHand(3))
agent2 = Agent(createHand(3))

# If Negative Agent 1 won most if positive agent 2 won most
for y in range(50):
    deck = constructDeck()

    # Start handout of cards
    agent1.setHand(createHand(3))
    agent2.setHand(createHand(3))

    # Start bidding phase 0 - 3
    for i in range(1,4):
        # Store bid
        agent1.setBid(agent1.reflexMem2Agent(agent2))
        agent2.setBid(agent2.reflexMemAgent(agent1))

        #Store bid of opponent
        agent1.addOpponentBid(agent2.getBid())
    #Store cards of opponent
    agent1.addOpponentCards(getHandValue(agent2.getHand()))

    # Showdown phase
    if getHandValue(agent1.getHand()) >= getHandValue(agent2.getHand()):
        agent1.setWinning(agent1.getTotalBid() + agent2.getTotalBid())
        agent2.setWinning((-1*agent2.getTotalBid()))
        print("Agent 1 won: ${}".format(agent1.getWinning()))
        
    else:
        agent2.setWinning(agent1.getTotalBid() + agent2.getTotalBid())
        agent1.setWinning((-1*agent1.getTotalBid()))
        print("Agent 2 won: ${}".format(agent2.getWinning()))
        
print("Winnings: Agent1 {} Agent2 {}".format(agent1.getWinning(),agent2.getWinning()))
print("Opponent Agent is a: " + str(agent1.getEnemyType()) + " Agent")
#plt.show()