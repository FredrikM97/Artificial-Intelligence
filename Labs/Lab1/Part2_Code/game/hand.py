from collections import Counter

class Hand:
    # Create a hand with the size of n
    def __init__(self, deck, n):
        self.deck = deck
        self.hand = deck.drawCards(n)

    # Remove characters from list
    def maskHand(self):
        mask = [list(c)[1] for c in self.hand]
        dic = {key: val +2 for val, key in enumerate(self.deck.rank)}
        return sorted([dic[s] for s in mask], reverse=True)


    # Get value of hand
    def getHandValue(self):
        hand = self.maskHand()
        return max(Counter(hand))<<(5*(max(Counter(hand).values())-1))