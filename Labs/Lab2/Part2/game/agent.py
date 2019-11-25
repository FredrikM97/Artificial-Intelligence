class Agent:
    def __init__(self):
        self.hand = []
        self.bid = 0
        self.totBid = 0
        self.balance = 0
        

################ Stuff to set #######################None
    # Params opponent
    def setBid(self, bid):
        self.setTotalBid(bid)
        self.bid = bid

    def setHand(self,hand):
        self.hand = hand

    # Should be private function
    def setTotalBid(self, bid):
        self.totBid += bid

    def addBalance(self, balance):
        self.balance += balance
        self.totBid = 0