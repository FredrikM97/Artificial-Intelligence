from itertools import product
from random import shuffle
from random import randint
import operator
import re
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
__author__ = 'fyt'

class Agent:
    def __init__(self, n):
        self.hand = createHand(n)
        self.bid = 0
        self.totBid = 0
        self.win = 0
        self.memBet = []

################ Stuff to set #######################
    def setBid(self, bid):
        self.setTotalBid(bid)
        self.bid = bid

    def setHand(self,n):
        if len(deck) > 3:
            self.hand = createHand(n)
        else:
            print("Not enough cards in deck")

    # Should be private function
    def setTotalBid(self, bid):
        self.totBid = self.totBid + bid

    def setWinning(self, win):
        self.win = self.win + win
        self.totBid = 0

    # Remember opponent earlier bets and previous losses
    def setMemory(self, bet):
        self.memBet.append(bet)
        len(self.memBet)

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
        return self.memBet

################ Agents #######################

    # Random bidding
    def randomAgent(self):
        return randint(0,50)

    # Fixed bidding
    def fixedAgent(self,n):
        return 10*n

    def reflexAgent(self,agent):
        agentHand = checkHands(self.getHand())
        return round(50*(1-(100/(agentHand+100))))

    # parameters: Second agent
    def reflexMemAgent(self, agent):
        agentHand = checkHands(self.getHand())
        memBet = agent.getBid()
        return round(50*(1-(memBet)/(agentHand+memBet)))

    def reflexMem2Agent(self, agent):
        agentHand = checkHands(self.getHand())
        memBet = agent.getBid()
        
        # Fixed agent
        if self.understandEnemy() == 1:
            return round(50*(1-(100)/(agentHand+100)))
        # Reflex agent
        elif self.understandEnemy() == 2:
            return round(50*(1-(memBet)/(agentHand+memBet)))
        # Random agent
        else:
            return round(50*(1-(100)/(agentHand+100)))
################ Help functions #######################

    # Realise what opponent it is playing against
    def understandEnemy(self):
        if len(self.getMemory())>5:
            if sum([self.getMemory()[0],self.getMemory()[1],self.getMemory()[2]]) == sum([self.getMemory()[3],self.getMemory()[4],self.getMemory()[5]]):
                #print("Its the Fixed Agent")
                return 1
            #elif self.getMemory()[0] != self.getMemory()[3]:
                #print("Its the random Agent")
                return 2
            # TODO If I bet low then he would more likely bet higher
            elif self.getMemory()[0] != self.getMemory()[3]:
                #print("Its the Reflex Agent")
                return 2
            else:
                return 0

################ Construct deck #######################

def constructDeck():
    suit = ["C","D","H","S"] 
    rank = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    deck = list(r + s for r, s in product(rank, suit))
    shuffle(deck)
    return deck

################ hand Actions #######################

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

def checkHands(agent):
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

winRate = []
deck = constructDeck()
agent1 = Agent(3)
agent2 = Agent(3)


# Statistic for plot range
for x in range(1):
    # If Negative Agent 1 won most if positive agent 2 won most
    agentWin = 0
    for y in range(100):
        deck = constructDeck()

        # Start handout of cards
        agent1.setHand(3)
        # Start bidding phase 0 - 3
        for i in range(1,4):
            # Store bid
            agent1.setBid(agent1.reflexMem2Agent(agent2))
            agent2.setBid(agent2.randomAgent())
            #Store bid of opponent
            agent1.setMemory(agent2.getBid())
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
    
print("Winnings \n Agent1 {} Agent2 {}".format(agent1.getWinning(),agent2.getWinning()))
agent1.understandEnemy()
#plt.hist(winRate, normed=True, bins=100)
#plt.show()
