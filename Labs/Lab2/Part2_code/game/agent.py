from .poker_environment import identify_hand, Types, AGENT_ACTIONS, Ranks

"""
Player class
"""
class PokerPlayer(object):
    def __init__(self, current_hand_=None, stack_=300, action_=None, action_value_=None):
        self.current_hand = current_hand_
        self.current_hand_type = []
        self.current_hand_strength = []
        self.stack = stack_
        self.action = action_
        self.action_value = action_value_

    """
    identify agent hand and evaluate it's strength
    """
    def evaluate_hand(self):
        self.current_hand_type = identify_hand(self.current_hand)
        self.current_hand_strength = Types[self.current_hand_type[0]]*len(Ranks) + Ranks[self.current_hand_type[1]]

    """
    return possible actions, fold if there is not enough money...
    """
    def get_actions(self):
        actions_ = []
        for _action_ in AGENT_ACTIONS:
            if _action_[:3] == 'BET' and int(_action_[3:])>=(self.stack):
                actions_.append('FOLD')
            else:
                actions_.append(_action_)
        return set(actions_)
