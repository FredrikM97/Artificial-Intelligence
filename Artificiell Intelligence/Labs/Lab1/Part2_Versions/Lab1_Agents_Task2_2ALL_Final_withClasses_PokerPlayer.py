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
    def __init__(self):
        self.hand = []
        self.bid = 0
        self.totBid = 0
        self.win = 0
        self.opponentBid = []
        self.opponentCardValue = []
        self.opponentType = "unknown"

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

    def setOpponentType(self, enemy):
        self.opponentType = enemy

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
    def getAgentType(self):
        
        # Chunk data
        if len(self.opponentBid) >= (3*5) and len(self.opponentBid) % 3 == 0 and len(self.opponentCardValue) > 0:
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
    def __init__(self):
        super().__init__()

    # Random bidding
    def bidding(self, board):
        self.setBid(randint(0,50))
        return self.getBid()
class fixedAgent(Agent):
    def __init__(self):
        super().__init__()
    # Fixed bidding
    def bidding(self, board):
        self.setBid(10*board.round)
        return self.getBid()
class reflexAgent(Agent):
    def __init__(self):
        super().__init__()
    # Check his own hand
    def bidding(self, board):
        agentHand = self.getHand().getHandValue()
        self.setBid(round(50*(1-(100/(agentHand+100)))))
        return self.getBid()
class reflexMemAgent(Agent):
    def __init__(self):
        super().__init__()

    # parameters: Opponent agent, check opponents betting
    def bidding(self, board):
        agentHand = self.getHand().getHandValue()
        opponentBid = self.opponent.getBid()
        self.setBid(round(50*(1-(opponentBid)/(agentHand+opponentBid))))
        return self.getBid()
class reflexMem2Agent(Agent):
    def __init__(self):
        super().__init__()
    # parameters: Opponent agent, Opponent with understanding of opponent
    def bidding(self, board):
        myHand = self.getHand().getHandValue()
        
        # Just assume that there is one other player :)
        if len(board.boardBids) == 0:
            opponentBid = 100
        else:
            for player in board.boardBids.keys():
                if player == self:
                    continue
                opponentBid = board.boardBids[player]
                
            
        
        temp = self.getAgentType() 

        if temp != "unknown":
            self.opponentType = temp    
        # reflex agent
        if self.opponentType == "reflex":
            self.setBid(round(50*(1-(opponentBid)/(myHand+opponentBid))))
        # Random agent, fixed agent or unknown agent
        else:
            self.setBid(round(50*(1-(100)/(myHand+100))))
        return self.getBid()
################ deck class #######################
class Deck:
    # Construct a deck and shuffle it
    def __init__(self):
        self.suit = ["C","D","H","S"] 
        self.rank = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        self.deck = list(r + s for r, s in product(self.rank, self.suit))
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
        self.hand = deck.drawCards(n)

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
        
        if(self.check_ThreeOfCards(hand)):
            return hand[0]<<(5*1)
        elif(self.check_Pair(hand)):
            return hand[0]<<(5*2)
        else:
            return self.check_HighCards(hand)

    ################ Check hand value #######################

    def check_HighCards(self, hand):
        return hand[2]

    def check_Pair(self, hand):
        return hand[0] == hand[1] or hand[1] == hand[2]

    def check_ThreeOfCards(self, hand):
        return hand[0] == hand[1] and hand[0] == hand[2] 

# Knows all info on the board
class Board:
    def __init__(self):
        self.winPot = 0
        self.boardBids = {}
        self.playerHands = {}
        self.deck = Deck()

    def __len__(self):
        return len(self.boardBids)

    def addBoardBids(self, player, bid):
        self.boardBids[player] = bid
    
    def setRound(self, round):
        self.round = round
    # Collect at end of round
    def sumWinPot(self):
        for bids in self.boardBids.values():
            self.winPot = self.winPot + bids

    def addPlayerHand(self, player):
        self.playerHands[player] = player.getHandValue()

################ Main loop #######################
class Simulation:
    def __init__(self):
       
        # Max two agents, choose between agents in Agent class
        self.createPlayers([reflexMem2Agent(), randomAgent()])
        self.cardAmount = 3 
        self.board = Board()
        
    def start(self):
        for y in range(50):
            self.board = Board()
            # Start handout of cards
            if self.handOut() == -1: break
            self.bidding()

            self.showdown()

        for player in self.players:
            print(str(self.players[player]) + ": Opponent is a: " + str(player.opponentType) + " Agent")
            print("Money: " + str(player.getWinning()))

    def createPlayers(self, agents): # Done
        self.players = {} 
        for i in range(0,len(agents)):
            self.players[agents[i]] = "Agent "+ str(i)

    def handOut(self): # Done
        if len(self.board.deck) >= (len(self.players)*self.cardAmount):
            for player in self.players:
                player.setHand(Hand(self.board.deck, self.cardAmount))
        else:
            print("Not enough cards in deck!")
            return -1

    def bidding(self):
        # Start bidding phase 0 - 3
        for i in range(1,4):
            self.board.setRound(i)
            # Store bid
            for player in self.players:
                self.board.addBoardBids(player, player.bidding(self.board))
                player.setWinning((-1*player.getBid()))

            #Store bid of opponent
            for player1 in self.players:
                for player2 in self.players:
                    if player1 == player2:
                        continue
                    player1.addOpponentBid(self.board.boardBids[player2])
                    break
                    
        self.board.sumWinPot()
    def showdown(self):
        for player1 in self.players:
            for player2 in self.players:
                if player1 == player2:
                    continue
                self.board.playerHands[player2] = player2.getHand().getHandValue()
                player1.addOpponentCards(self.board.playerHands[player2])
                break                            
        
        # Showdown phase
        for player1 in self.players:
            for player2 in self.players:  
                if player1.getHand().getHandValue() > player2.getHand().getHandValue():
                    player1.setWinning(self.board.winPot)
                    #print("Winner: " + str(self.players[player1]))
                else:
                    player2.setWinning(self.board.winPot)
                    #print("Winner: " + str(self.players[player2]))
       
simulation = Simulation()
simulation.start()