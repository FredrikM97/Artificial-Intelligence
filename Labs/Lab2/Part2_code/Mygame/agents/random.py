from game.agent import Agent
from random import randint

class randomAgent(Agent):
    def __init__(self):
        super().__init__()

    # Random bidding
    def bidding(self, board):
        self.setBid(randint(0,50))
        return self.bid
