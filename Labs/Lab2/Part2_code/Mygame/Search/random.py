from game.agent import Agent

class RandomSearch(Agent):
    def __init__(self):
        super().__init__()
        self.opponents = {}

    def update(self,board):
        for key in board.playerHands.keys():
            # If player folded then it should no longer add values or try
            if key == self: continue
            if key not in board.game.player: del self.opponents[key]

            self.addOpponent(key)
            self.opponents[key]['cardVal'].append(board.playerHands[key])
            self.opponents[key]['bid'].extend(board.boardBids[key]) 
    
    # Update what action the opponent did opponent
    def action(self, board, player):
        if player == self: return 1
        self.addOpponent(player)
        self.opponents[player]['action'].append(player)

    def getOpponents(self):
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
            'cardVal':[],
            'actions':[]
        }
        return 0
    
    def bidding(self, board):
        bids = [5,10,25]

## TODO
# Write bidding tree
# Analyse how example is done