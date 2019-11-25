from game.agent import Agent

class RandomSearch(Agent):
    def __init__(self):
        super().__init__()
        self.opponentsAction
        # Oppoents action
        # Opponents Bet

    def update(self,board):
        for key in board.playerHands.keys():
            if key == self: continue
            # Get opponents action

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
            'cardVal':[]
        }
        return 0