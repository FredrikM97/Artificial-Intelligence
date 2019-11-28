import poker_environment as pe_
from poker_environment import AGENT_ACTIONS, BETTING_ACTIONS
from player import PokerPlayer
import copy

"""
Game State class
"""
class GameState(object):
    def __init__(self,
                 nn_current_hand_=None,
                 nn_current_bidding_=None,
                 phase_ = None,
                 pot_=None,
                 acting_agent_=None,
                 parent_state_=None,
                 children_state_=None,
                 agent_=None,
                 opponent_=None):

        self.nn_current_hand = nn_current_hand_
        self.nn_current_bidding = nn_current_bidding_
        self.phase = phase_
        self.pot = pot_
        self.acting_agent = acting_agent_
        self.parent_state = parent_state_
        self.children = children_state_
        self.agent = agent_
        self.opponent = opponent_
        self.showdown_info = None
    # Needed to compare
    def __lt__(self, other):
        return 1
    def __le__(self, other):
        return 1

    """
    draw 10 cards randomly from a deck
    """
    def dealing_cards(self):
        agent_hand, opponent_hand = pe_.generate_2hands()
        self.agent.current_hand = agent_hand
        self.agent.evaluate_hand()
        self.opponent.current_hand = opponent_hand
        self.opponent.evaluate_hand()
        #self.showdown_info = None

    """
    draw 10 cards from a fixed sequence of hands
    """
    def dealing_cards_fixed(self):
        self.agent.current_hand = pe_.fixed_hands[self.nn_current_hand][0]
        self.agent.evaluate_hand()
        self.opponent.current_hand = pe_.fixed_hands[self.nn_current_hand][1]
        self.opponent.evaluate_hand()

    """
    SHOWDOWN phase, assign pot to players
    """
    def showdown(self):

        if self.agent.current_hand_strength == self.opponent.current_hand_strength:
            self.showdown_info = 'draw'
            if self.acting_agent == 'agent':
                self.agent.stack += (self.pot - 5) / 2. + 5
                self.opponent.stack += (self.pot - 5) / 2.
            else:
                self.agent.stack += (self.pot - 5) / 2.
                self.opponent.stack += (self.pot - 5) / 2. + 5
        elif self.agent.current_hand_strength > self.opponent.current_hand_strength:
            self.showdown_info = 'agent win'
            self.agent.stack += self.pot
        else:
            self.showdown_info = 'opponent win'
            self.opponent.stack += self.pot

    # print out necessary information of this game state
    def print_state_info(self):

        print('************* state info **************')
        print('nn_current_hand', self.nn_current_hand)
        print('nn_current_bidding', self.nn_current_bidding)
        print('phase', self.phase)
        print('pot', self.pot)
        print('acting_agent', self.acting_agent)
        print('parent_state', self.parent_state)
        print('children', self.children)
        print('agent', self.agent)
        print('opponent', self.opponent)

        if self.phase == 'SHOWDOWN':
            print('---------- showdown ----------')
            print('agent.current_hand', self.agent.current_hand)
            print(self.agent.current_hand_type, self.agent.current_hand_strength)
            print('opponent.current_hand', self.opponent.current_hand)
            print(self.opponent.current_hand_type, self.opponent.current_hand_strength)
            print('showdown_info', self.showdown_info)

        print('----- agent -----')
        print('agent.current_hand',self.agent.current_hand)
        print('agent.current_hand_type',self.agent.current_hand_type)
        print('agent.current_hand_strength',self.agent.current_hand_strength)
        print('agent.stack',self.agent.stack)
        print('agent.action',self.agent.action)
        print('agent.action_value',self.agent.action_value)

        print('----- opponent -----')
        print('opponent.current_hand', self.opponent.current_hand)
        print('opponent.current_hand_type',self.opponent.current_hand_type)
        print('opponent.current_hand_strength',self.opponent.current_hand_strength)
        print('opponent.stack',self.opponent.stack)
        print('opponent.action',self.opponent.action)
        print('opponent.action_value',self.opponent.action_value)
        print('**************** end ******************')

## Calculate the right path from goal to start
def pathFunc(newMap, goal):
    example_solved_path = []
    node = newMap[goal]
    cords = goal
    while node['parent'] != None:
        example_solved_path.insert(0, cords)
        node = newMap[node['parent']]
        cords = node['parent']
    return example_solved_path

"""
Game flow:
Two agents will keep playing until one of them lose 100 coins or more.
"""
from algorithmSearch.search import Search
class simulation:
    def __init__(self, MAX_HANDS=4, goal=100, rounds= 1, visualMode=False, algorithm=0, heuristic='big'):
        self.MAX_HANDS = MAX_HANDS
        self.INIT_AGENT_STACK = 400
        self.step_avg = 0
        self.depth_avg = 0
        self.rounds = rounds
        self.visualMode = visualMode
        self.algorithm = algorithm
        self.heuristic = heuristic
        self.goal = goal
        self.depthLimit = 40

    def run(self):
        for x in range(0, self.rounds):
            self.init()
            self.init_state.dealing_cards()
            self.data = Search(self.init_state, self.algorithm, self.goal, self.heuristic, 
            
            self.depthLimit).search()
            self.printGameInfo()

    def init(self):
        self.nn_level = 0
        # initialize 2 agents and a game_state
        self.agent = PokerPlayer(current_hand_=None, stack_=self.INIT_AGENT_STACK, action_=None, action_value_=None)
        self.opponent = PokerPlayer(current_hand_=None, stack_=self.INIT_AGENT_STACK, action_=None, action_value_=None)


        self.init_state = GameState(nn_current_hand_=0,
                            nn_current_bidding_=0,
                            phase_ = 'INIT_DEALING',
                            pot_=0,
                            acting_agent_=None,
                            agent_=self.agent,
                            opponent_=self.opponent,
        )

    def printGameInfo(self):
        path = pathFunc(self.data.node, list(self.data.node)[-1])
        
        print('------------ print game info ---------------')
        if not len(list(self.data.node)) == '0':
            print("Agent won")
            
            if self.visualMode: self.printGameStatistics(path)
            
            self.step_avg += self.data.steps
            self.depth_avg +=self.data.g
        else:
            print("Agent lost")

    def printGameStatistics(self,path):
        for state in path:
            agent = state.agent
            opponent = state.opponent
            val = state.opponent.action_value
            pot = state.pot
            info = state.showdown_info
            hand = state.nn_current_hand
            phase = state.phase
            print("\n--- Agent ---")
            print("stack: ", agent.stack, "action: ", agent.action)
            print("\n---Opponent---")
            print("stack: ", opponent.stack, "action: ", opponent.action)
            print("pot: ",pot, "phase: ", phase)
            self.nn_level += 1

if __name__ == "__main__":
    game = simulation(4,100, 10, False, 'A*', 'many')
    game.run()

    print("---Statistics----")
    print("Type: ", game.data.type, "\nDepth:", game.depth_avg/game.rounds,"\nAvg Expanded: ", game.step_avg/game.rounds)
