from collections import Counter

class Hand:
    # Create a hand with the size of n
    def __init__(self, deck, n):
        self.deck = deck
        self.hand = deck.drawCards(n)

    # Remove characters from list
    def maskHand(self):
        mask = [list(c) for c in self.hand]
        print(mask)
        dic = {key: val +2 for val, key in enumerate(self.deck.rank)}
        
        return sorted([dic[s] for s in mask], reverse=True)


    # Get value of hand
    def getHandValue(self):
        hand = self.maskHand()
        '''
        Types = {
            'HighCard':      1,
            'OnePair':       2,
            'TwoPairs':      3,
            '3OfAKind':      4,
            'Straight':      5, (stege)
            'Flush':         6, (alla av samma färg)
            'FullHouse':     7, (tre av samma och två av ett annat - kåk)
            '4OfAKind':      8,
            'StraightFlush': 9 (stege av samma färg)
        }
        '''
        #print(hand)
        # Fix colors   
        # Handles up to 5 pair
        return max(Counter(hand))<<(5*(max(Counter(hand).values())-1))
