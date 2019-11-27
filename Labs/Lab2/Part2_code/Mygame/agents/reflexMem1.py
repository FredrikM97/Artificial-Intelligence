from game.agent import Agent
from game.observer import Observer

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
