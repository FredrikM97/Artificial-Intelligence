from random import shuffle
from itertools import product

class Deck:
    # Construct a deck and shuffle it
    def __init__(self):
        self.suit = ["C","D","H","S"] 
        self.rank = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
        self.deck = list(s + r for (s, r) in product(self.suit, self.rank))
        shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def drawCards(self, n):
        hand = self.deck[:n]
        del self.deck[-n:], self.deck[:n]
        return hand
