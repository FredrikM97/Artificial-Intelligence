import random
import ClientBase
from copy import deepcopy
from deuces import Card, Evaluator# https://github.com/FredrikM97/deuces python3

class Agent:
    "Template class for poker agents"
    def __init__(self, name):
        self.name = name
        self.round = 0
        self.Chips = 0
        self.CurrentBet = 0
        self.Ante = 0
        self.CurrentHand = []
        self.maxBet = 1
        self.minRaise = 1
        self.players = {}
        
    def queryOpenAction(self, minimumPotAfterOpen, playersCurrentBet, playersRemainingChips):
        '''
        Called during the betting phases of the game when the player needs to decide what open
        action to choose.
        '''
        raise NotImplementedError
   

    def queryCallRaiseAction(self, maximumBet, minimumAmountToRaiseTo, playersCurrentBet, playersRemainingChips):
        '''
        Called during the betting phases of the game when the player needs to decide what call/raise
        action to choose.
        '''
        raise NotImplementedError

    def queryCardsToThrow(self, _hand):
        "Strategy to throw cards"
        raise NotImplementedError
    
    def bet(self,number):
        if issubclass(number.__class__, dict): 
            print("Yaarr, you caught my arrow:",number)
        #assert number <= self.Chips
        self.Chips -= number
        self.CurrentBet += number
   
    def openAction(self, bet=0, **kwargs):
        self.bet(bet)

    def checkAction(self, **kwargs):
        pass # yes, do nothing

    def allinAction(self, **kwargs):
       self.bet(self.Chips)
        
    def foldAction(self, **kwargs):
        self.CurrentBet = 0

    def callAction(self, _maximumBet=0, _playersCurrentBet=0, **kwargs):
        diff = _maximumBet - _playersCurrentBet
        self.bet(diff)

    def raiseAction(self, bet=0, **kwargs):
        self.bet(bet)

class ml_agent(Agent):
    def __init__(self, name="Classy"):
        Agent.__init__(self, name)

    def queryOpenAction(self, min_pot_after_open, current_bet, remaining_chips):
        # Check what actions we can do
        possible_actions = [
            ClientBase.BettingAnswer.ACTION_CHECK,
            ClientBase.BettingAnswer.ACTION_ALLIN,
        ]
        can_open = current_bet + remaining_chips > min_pot_after_open
        bet = 10 + min_pot_after_open \
        if current_bet + remaining_chips + 10> min_pot_after_open \
        else min_pot_after_open
        if can_open: possible_actions.append(ClientBase.BettingAnswer.ACTION_OPEN, bet)

        # Evaluate actions
        
        
    def get_features(self):
        feature = [self.hand]
        """ TODO: finish this part
        {player1:{hand,chips,Actions},player2:{hand,chips,Actions}}

        

        feature.extend(["Every players chip"])
        feature.extend(["every players actions"])

        ml.predict(feature)
        """
        chips = [self.Chips]
        actions = self.players[self.name]['action']
        playerCopy = deepcopy(self.players)
        del playerCopy[self.name]

        for info in playerCopy.values():
            chips.append()

            
        pass

class RandomAgent(Agent):
    def __init__(self, name="Random"):
        Agent.__init__(self, name)

    def queryOpenAction(self, _minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
        print("Player requested to choose an opening action.")
       
        def canOpen():    
            if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
                if _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen: 
                    bet = (random.randint(0, 10) + _minimumPotAfterOpen)
                else: 
                    bet = _minimumPotAfterOpen
                return ClientBase.BettingAnswer.ACTION_OPEN, bet
            else:
                return ClientBase.BettingAnswer.ACTION_CHECK
            
        action = {
            0: ClientBase.BettingAnswer.ACTION_CHECK,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
        }.get(random.randint(0, 2), canOpen())

        switch = {
            ClientBase.BettingAnswer.ACTION_OPEN:self.openAction,
            ClientBase.BettingAnswer.ACTION_CHECK:self.checkAction, 
            ClientBase.BettingAnswer.ACTION_ALLIN:self.allinAction
        }

        if issubclass(action.__class__,str):
            switch[action]()  
        else: 
            switch[action[0]](bet=action[1])

        return action
    

    def queryCallRaiseAction(self, _maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
        print("Player requested to choose a call/raise action.")

        def canRaise():
            # If can raise
            if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
                # do raise
                if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo: 
                    bet = (random.randint(0, 10) + _minimumAmountToRaiseTo) 
                else: 
                    bet = _minimumAmountToRaiseTo
                return ClientBase.BettingAnswer.ACTION_RAISE, bet
            else:
                return ClientBase.BettingAnswer.ACTION_FOLD

        action =  {
            0: ClientBase.BettingAnswer.ACTION_FOLD,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
            2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
        }.get(random.randint(0, 3), canRaise())

        switch = {
            ClientBase.BettingAnswer.ACTION_FOLD:self.foldAction,
            ClientBase.BettingAnswer.ACTION_CALL:self.callAction, 
            ClientBase.BettingAnswer.ACTION_ALLIN:self.allinAction,
            ClientBase.BettingAnswer.ACTION_RAISE:self.raiseAction
        }

        args={'_maximumBet':_maximumBet,'_playersCurrentBet':_playersCurrentBet}
        if issubclass(action.__class__,str):
            switch[action](**args)  
        else:
            switch[action[0]](bet=action[1], **args)

        return action

    def updateAgent(self, currentBet):
        self.CurrentBet = currentBet
        self.Chips -= currentBet

    def queryCardsToThrow(self, _hand):
        print("Requested information about what cards to throw")
        print(_hand)
        return _hand[random.randint(0,4)] #+ ' '
    '''
    [targetHandStrength, targetChips, targetWin, p1Chips,p2Chips, targetAction1,targetAction2, p1Action1,p1Action2, p2Action1, p2Action2]  
    '''
    def addGameStatus(self, player=None, action=None, data=None, **kwarg):
        ''' Add status of the game to gameStatus '''   
        states = [ 
            'hand',
            'chips'
        ]
        actions = [ 
            'open',
            'call',
            'check',
            'raise',
            'fold',
            'allin'
        ]
            
        if (player == self.name or action == 'round'): # If data comes from agent
            try:
                self.__dict__[action] = int(data) # Overwrite local data
            except:
                print("True face:",data,type(data))
        
        if player not in self.players:
            self.players.update({player:{'hand':0,'chips':0, 'action':[]}})

        if action in actions: # Add action to player if it exists
            self.players[player]['action'].append(action)
            
        elif action in states:
            if action == 'hand':  # Evaluate if hand is action
                data = data[0:5] # In case server gets confused and send wrong message
                hand = [Card.new(x) for x in data]
                data = Evaluator().evaluate([], hand) # Lower the better

            self.players[player][action] = data
    