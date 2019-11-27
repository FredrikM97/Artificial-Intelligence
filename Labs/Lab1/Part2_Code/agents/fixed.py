from game.agent import Agent

class fixedAgent(Agent):
    def __init__(self):
        super().__init__()
    # Fixed bidding
    def bidding(self, board):
        self.setBid(5 + 10*board.round)
        return self.bid