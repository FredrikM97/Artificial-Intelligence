from .deck import Deck
from .hand import Hand
from .observer import Observer
# Knows all info on the board
class Board:
    def __init__(self, game):
        self.winPot = 0
        self.boardBids = {}
        self.playerHands = {}
        self.deck = Deck()
        self.game = game
        self.round = 0

    def __len__(self):
        return len(self.boardBids)

    def handOut(self, cardAmount): # Done
        if len(self.deck) >= (len(self.game.players)*cardAmount):
            for player in self.game.players:
                self.boardBids[player] = []
                player.setHand(Hand(self.deck, cardAmount))
        else:
            return -1

        return self
        
    # Only memorise bit of one Round!
    def bid(self):
        self.round = self.round + 1
        for player in self.game.players:
            self.boardBids[player].append(player.bidding(self))
            player.addBalance((-1*player.bid))  
            self.sumWinPot(player.bid)
        return self

    def showdown(self):    
        # Add each players hand to the board player  hand
        for player in self.game.players:
            self.playerHands[player] = player.hand.getHandValue()

        for player in self.game.players:
            if issubclass(player.__class__, Observer): 
                player.update(self)

        # Showdown phase - Get winner
        winner = sorted(self.playerHands.items(), key=lambda x: x[1])[-1][0]
        for player in self.game.players:
            if player == winner:
                player.addBalance(self.winPot)

        return self

    def sumWinPot(self, bid):
        self.winPot = self.winPot + bid
