from game.agent import Agent

class reflexAgent(Agent):
    def __init__(self):
        super().__init__()
    # Check his own hand
    def bidding(self, board):
        agentHand = self.hand.getHandValue()
        self.setBid(round(50*(1-(100/(agentHand+100)))))
        return self.bid