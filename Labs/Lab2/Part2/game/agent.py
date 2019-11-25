class Agent:
    def __init__(self, balance=100):
        self.hand = []
        self.bid = 0
        self.totBid = 0
        self.balance = balance

################ Stuff to set #######################

    # Params opponent
    def setBid(self, bid):
        if self.balance > bid:
            self.bid = bid
            self.setTotalBid(bid)
        else: 
            return -1
        
    def setHand(self,hand):
        self.hand = hand

    # Should be private function
    def setTotalBid(self, bid):
        self.totBid += bid

    def addBalance(self, balance):
        if self.balance <= balance: return -1 
        self.balance += balance
        self.totBid = 0