
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
        self.hand = [Card.new(card) for card in hand]
        evaluator = Evaluator()
        AGENT.hand_rank = evaluator.evaluate([*AGENT.hand])
        AGENT.hand_class = evaluator.class_to_string(evaluator.get_rank_class(AGENT.hand_rank))
        AGENT.hand_fcrp = evaluator.get_five_card_rank_percentage(AGENT.hand_rank)
'''

class devolution:
    def __init__(self):
        # open file and fetch matrix if there's one else make a new one
        try:
            f = open('evo_data')
        except:
            open('evo_data', mode='x')
            f = open('evo_data', mode='a')
            f.write
