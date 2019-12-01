from game.agent import PokerPlayer
from algorithmSearch.search import Search
from game.gameState import GameState

class Simulation:
    def __init__(self, MAX_HANDS=4, goal=100, rounds= 1, visualMode=False, depthLimit = 20 , algorithm='BFS', strategy='MANY'):
        self.MAX_HANDS = MAX_HANDS
        self.INIT_AGENT_STACK = 400
        self.step_avg = 0
        self.pathLength_avg = 0
        self.rounds = rounds
        self.visualMode = visualMode
        self.algorithm = algorithm
        self.strategy = strategy
        self.goal = goal
        self.depthLimit = depthLimit
        self.winStreak = 0

    def run(self):
        for x in range(0, self.rounds):
            self.init()
            self.init_state.dealing_cards()
            self.data = Search(self.init_state, \
                                self.algorithm, \
                                self.goal,      \
                                self.strategy, \
                                self.depthLimit \
                                ).search()

            self.printGameInfo()

    def init(self):
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
        if not self.data == -1:
            path = self.pathFunc(self.data.node, list(self.data.node)[-1])
            
            if self.visualMode: self.printGameStatistics(path)
            
            self.step_avg += self.data.steps
            self.pathLength_avg +=self.data.g
            self.winStreak += 1
        
    def printGameStatistics(self,path):
        print(f'\n------------ print game info --------------- \
        \nAgent won!')

        for state in path:
            agent = state.agent
            opponent = state.opponent
            print(f'\
            \n--- Agent --- \
            \nstack: {agent.stack}, action: {agent.action} \
            \n--- Opponent --- \
            \nstack; {opponent.stack}, action: {opponent.action} \
            \nPot: {state.pot}, Phase: {state.phase}')
        
    ## Calculate the right path from goal to start
    def pathFunc(self, newMap, goal):
        example_solved_path = []
        node = newMap[goal]
        cords = goal
        while node['parent'] != None:
            example_solved_path.insert(0, cords)
            node = newMap[node['parent']]
            cords = node['parent']
        return example_solved_path