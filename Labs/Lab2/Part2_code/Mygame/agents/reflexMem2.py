from game.agent import Agent
from game.observer import Observer
import numpy as np


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
    