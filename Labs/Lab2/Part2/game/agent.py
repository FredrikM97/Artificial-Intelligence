class Agent:
    def __init__(self, balance=100):
        self.hand = []
        self.bid = 0
        self.totBid = 0
        self.balance = balance

################ Stuff to set #######################
    def call(self):
        # Possible to call as long bid is above 0
        if self.bid > 0:
            self.bid = 5    
            self.setTotalBid(self.bid)
        else:
            return -1
    def fold(self):
        pass

    # Params opponent
    def setBid(self, bid):
        self.bid = bid
        self.setTotalBid(bid)
        
    def setHand(self,hand):
        self.hand = hand

    # Should be private function
    def setTotalBid(self, bid):
        self.totBid += bid

    def addBalance(self, balance):
        self.balance += balance
        self.totBid = 0