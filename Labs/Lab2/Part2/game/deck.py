from itertools import product
from random import shuffle, randint

################ deck class #######################
class Deck:
    # Construct a deck and shuffle it
    def __init__(self):
        self.suit = ["C","D","H","S"] 
        self.rank = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
        self.deck = list(r + s for (r, s) in product(self.rank, self.suit))
        shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def drawCards(self, n):
        hand = self.deck[:n]
        del self.deck[-n:], self.deck[:n]
        return hand
