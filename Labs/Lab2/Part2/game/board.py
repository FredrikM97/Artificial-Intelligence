from .deck import Deck
from .hand import Hand
from .observer import Observer
# Knows all info on the board
class Board:
    def __init__(self, game):
        self.winPot = 0
        self.boardBids = {}
        self.playerHands = {}
        self.playerActions = {}
        self.deck = Deck()
        self.game = game
        self.round = 0

    def __len__(self):
        return len(self.boardBids)

    def handOut(self, cardAmount): # Done
        if len(self.deck) >= (len(self.game.players)*cardAmount):
            for player in self.game.players:
                self.boardBids[player] = []
                self.playerActions[player] = []
                player.setHand(Hand(self.deck, cardAmount))
        else:
            return -1

        return self
        
    # Only memorise bit of one Round!
    def bid(self):
        self.round = self.round + 1
        for player in self.game.players:

                if player.balance <= 0:
                    continue
                # Action and bid
                data = player.bidding(self)
                action = data[0] # What kind of action
                bid = 0 
                
                if action == "bid":
                    bid = data[1] 
                elif action == "call":
                    if data[1] > 5: 
                        bid = 5
                    else: 
                        print("Your bid is to low!!")      
                elif action == "fold": # Delete user if he fold
                    del player
                
                # If balance is to low -> remove player
                if player.addBalance((-1*bid)) == -1:
                    print("Player: ", player.name,  "is out of money")
                    del player
                    continue

                self.sumWinPot(bid) # Add to win pot
                self.boardBids[player].append(bid) # Store bid for one round
                self.playerActions[player].append(action) # Store the action for one round

                # Tell everyone the others action
                for player1 in self.game.players:
                    if issubclass(player1.__class__, Observer): 
                        player1.action(self, player)

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
