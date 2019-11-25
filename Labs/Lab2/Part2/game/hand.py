from collections import Counter, defaultdict
class Hand:
    # Create a hand with the size of n
    def __init__(self, deck, n):
        self.cardsOnHand = n
        self.deck = deck
        self.hand = deck.drawCards(n)
        self.cardOrder = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10,"J":11, "Q":12, "K":13, "A":14}
        
        self.handValues = {
            9:"straight-flush",
            8:"four-of-a-kind", 
            7:"full-house", 
            6:"flush", 
            5:"straight", 
            4:"three-of-a-kind", 
            3:"two-pairs", 
            2:"one-pair", 
            1:"highest-card"
        }
        self.sortedHand = self.sortHand()
        
    # Remove characters from list
    def sortHand(self):
        mask = [list(c)[0] for c in self.hand]
        
        dic = {key: val+2 for val, key in enumerate(self.deck.rank)}
        
        return sorted([dic[s] for s in mask], reverse=True)

    # Get value of hand
    def getHandValue(self):
        # Sorted and removed Type
        hand = self.sortHand()

        return max(Counter(hand))<<(5*(max(Counter(hand).values())-1))
        #self.handValues[check_hand()]



    # Expected return: ['TwoPair', 'J', 'C']
    def check_hand(self):
        if self.straight_flush():
            return 9
        if self.four_of_a_kind():
            return 8
        if self.full_house():
            return 7
        if self.flush():
            return 6
        if self.straight():
            return 5
        return self.max_pairs()

    def countValues(self):
        values = [i[0] for i in self.hand]
        cards = Counter(values) 

        return [next(iter(Counter(values)))]

    # Ladder + same color
    def straight_flush(self):
        return self.flush() and self.straight()


    def four_of_a_kind(self):
        cnt = self.countValues()
        return max(cnt) == 4

    # If 3 + 2 cards then it is full house
    def full_house(self):
        cnt = self.countValues()
        max(cnt) + min(cnt) == self.cardsOnHand

    # If all is same color
    def flush(self):
        suits = [h[0] for h in self.hand]
        return len(set(suits)) == 1

    # Get max pairs (2-3 pairs) and max value
    def max_pairs(self):
        cnt = self.countValues()
        return max(cnt)    

    # Check if ladder
    def straight(self):
        values = [i[0] for i in self.hand]
        cnt = 0
        leng = len(values)
        for x in range(0,leng-1):
            if int(values[x]) - 1 == int(values[x+1]):  
                cnt +=1
        
        # If they are the same size then we now it
        return cnt == leng-1