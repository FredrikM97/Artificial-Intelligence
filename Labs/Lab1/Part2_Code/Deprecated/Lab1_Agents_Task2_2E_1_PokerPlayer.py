from itertools import product
from random import shuffle
from random import randint
import operator
import re
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
__author__ = 'fyt'

# identify if there is one or more pairs in the hand

    #HandCategory = []

    #functionToUse = identifyHand

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}

# 2 example poker hands
# CurrentHand1 = ['Ad', '2s', '2c']
# CurrentHand2 = ['5s', '5c', '5d']

# identify hand category using IF-THEN rule


'''
def identifyHand(Hand_):
    for c1 in Hand_:
        for c2 in Hand_:
            if (c1[0] == c2[0]) and (c1[1] < c2[1]):
                yield dict(name='pair',rank=c1[0],suit1=c1[1],suit2=c2[1])

# Print out the result
def analyseHand(Hand_):
    for category in functionToUse(Hand_):
        print('Category: ')
        for key in "name rank suit1 suit2".split():
            print( key,"=",category[key])
'''      

################ Create agent object #######################
class Agent:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        self.totBid = 0
        self.win = 0

    def setBid(self, bid):
        self.setTotalBid(bid)
        self.bid = bid
        
    # Should be private function
    def setTotalBid(self, bid):
        self.totBid = self.totBid + bid

    def setWinning(self, win):
        self.win = self.win + win
        self.totBid = 0

    def getBid(self):
        return self.bid

    def getTotalBid(self):
        return self.totBid

    def getHand(self):
        return self.hand

    def getWinning(self):
        return self.win

################ Construct deck #######################

def constructDeck():
    suit = ["C","D","H","S"] 
    rank = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    cards = list(r + s for r, s in product(rank, suit))
    shuffle(cards)
    return cards

################ Check the hand #######################

def getHand(n):
    newHand = cards[:n]
    del cards[-n:], cards[:n]
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

def checkHands(agent):
    mask = maskHand(agent)
    if(check_ThreeOfCards(mask)):
        return mask[0]<<(5*1)
    elif(check_Pair(mask)):
        return mask[0]<<(5*2)
    else:
        return check_HighCards(mask)

def check_HighCards(hand):
    return hand[2]

def check_Pair(hand):
    return hand[0] == hand[1] or hand[1] == hand[2]

def check_ThreeOfCards(hand):
    return hand[0] == hand[1] and hand[0] == hand[2] 

################ Agents #######################

# Random bidding
def randomAgent():
    return randint(0,50)

# Fixed bidding
def fixedAgent(n):
    return 10*n

def reflexAgent(agent):
    agentHand = checkHands(agent.getHand())
    print(agentHand)
    decision = round(50*(1-(100/(agentHand+100))))
    return decision

# parameters: First agent, second agent
def reflexMemAgent(agent_1, agent_2):
    agentHand = checkHands(agent_1.getHand())
    oppBet = agent_2.getBid()
    print(agentHand)
    decision = round(50*(1-(oppBet)/(agentHand+oppBet)))
    return decision

winRate = []

# Statistic for plot range
for x in range(1):
    # If Negative Agent 1 won most if positive agent 2 won most
    agentWin = 0
    for y in range(1):
        # Start handout of cards
        cards = constructDeck()
        agent1 = Agent(getHand(3), 0)
        agent2 = Agent(getHand(3), 0)

        # Start bidding phase 0 - 3
        for i in range(1,4):
            # Set betting agent
            agent1.setBid(reflexAgent(agent1))
            agent2.setBid(reflexMemAgent(agent2, agent1))
            print('Phase:{} Agent1: ${} Agent2: ${})'.format(x, agent1.getBid(), agent2.getBid()))


        # Showdown phase
        if checkHands(agent1.getHand()) >= checkHands(agent2.getHand()):
            agent1.setWinning(agent1.getTotalBid() + agent2.getTotalBid())
            agent2.setWinning((-1*agent2.getTotalBid()))
            agentWin = agentWin - 1
            print("Agent 1 won: ${}".format(agent1.getWinning()))
            
        else:
            agent2.setWinning(agent1.getTotalBid() + agent2.getTotalBid())
            agent1.setWinning((-1*agent1.getTotalBid()))
            agentWin = agentWin + 1
            print("Agent 2 won: ${}".format(agent2.getWinning()))
            
    winRate.append(agentWin)
    

#plt.hist(winRate, normed=True, bins=100)
#plt.show()
