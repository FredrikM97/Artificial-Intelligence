
'''
TODO:
Parameters: {Time, cntMessages, Latest received message, MaxBet, HandStrength}
Time: Relative latest drop
cntMessages: Number of messages
Latest received message: Valid message from server
MaxBet: max bet in pot
HandStrength: Agents hand strength

One hot encoding- latest message
'''
'''
# from deuces import Evaluator, Card in order to use dis
def evaluateHand(self, hand):
        self.hand = []
        for card in hand:
            self.hand.append(Card.new(card))
        evaluator = Evaluator()
        AGENT.hand_rank = evaluator.evaluate([AGENT.hand[0], AGENT.hand[1], AGENT.hand[2]],
                                             [AGENT.hand[3], AGENT.hand[4]])
        AGENT.hand_class = evaluator.class_to_string(evaluator.get_rank_class(AGENT.hand_rank))
        AGENT.hand_fcrp = evaluator.get_five_card_rank_percentage(AGENT.hand_rank)
'''