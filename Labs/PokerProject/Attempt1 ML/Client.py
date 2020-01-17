import random
import ClientBase
from copy import deepcopy
from deuces import Card, Evaluator# https://github.com/FredrikM97/deuces python3
import evolution.ml as ml
from typing import List
from copy import copy

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

    def hand2Strength(self,hand):
        hand = hand[0:5] # In case server gets confused and send wrong message
        hand = [Card.new(x) for x in hand]
        return Evaluator().evaluate([], hand) # Lower the better

    '''
    [targetHandStrength, targetChips, targetWin, p1Chips,p2Chips, targetAction1,targetAction2, p1Action1,p1Action2, p2Action1, p2Action2]  
    '''
    def addGameStatus(self, player=None, action=None, data=None, **kwarg):
        ''' Add status of the game to gameStatus '''   
        states = [ 
            'chips'
        ]
        actions = [ 
            'open',
            'call',
            'check',
            'raise',
            'fold',
            'all-in'
        ]
        
        if (player == self.name or action == 'round'): # If data comes from agent
            try:
                self.__dict__[action] = int(data) # Overwrite local data
            except:
                print("True face:",data,type(data))
        
        if player not in self.players and player != None:
            self.players.update({player:{'chips':0, 'action':['None', 'None']}})

        if action in actions: # Add action to player if it exists
            self.players[player]['action'].append('Player_'+action[0].upper()+action[1:])
            
        elif action in states:
            self.players[player][action] = int(data)

class ml_agent(Agent):
    def __init__(self, name="Classy"):
        Agent.__init__(self, name)
        self.model, self.processes, self.args = ml.create_model('evolution/minedData.txt')

    def queryOpenAction(self, min_pot_after_open, current_bet, remaining_chips):
        # Check what actions we can do
        possible_actions = [
            (ClientBase.BettingAnswer.ACTION_CHECK, 0),
            (ClientBase.BettingAnswer.ACTION_ALLIN, 0),
        ]
        can_open = current_bet + remaining_chips > min_pot_after_open
        bet = 10 + min_pot_after_open \
        if current_bet + remaining_chips + 10> min_pot_after_open \
        else min_pot_after_open
        if can_open: possible_actions.append((ClientBase.BettingAnswer.ACTION_OPEN, bet))

        # Evaluate actions
        prob_of_action = [(self.model.predict_proba(self.get_feature(action))[0][1], action, value) \
            for action, value in possible_actions]
        prob, best_action, value = max(prob_of_action, key=lambda x:x[0])
        #print(prob_of_action)
        print('prob', prob, 'best_action', best_action, 'value', value)

        # Inform agent of what we do
        switch = {
            ClientBase.BettingAnswer.ACTION_OPEN:self.openAction,
            ClientBase.BettingAnswer.ACTION_CHECK:self.checkAction, 
            ClientBase.BettingAnswer.ACTION_ALLIN:self.allinAction
        }
        switch[best_action](bet=value)
        self.players[self.name]['action'].append(best_action) #FIXME: ugly hotfix

        # Inform server
        if best_action == ClientBase.BettingAnswer.ACTION_OPEN:
            return (best_action,value)
        return best_action

    def queryCallRaiseAction(self, max_bet, minimum_to_raise_to, current_bet, remaining_chips):
        # Check what actions we can do
        possible_actions = [ 
            (ClientBase.BettingAnswer.ACTION_FOLD, 0),
            (ClientBase.BettingAnswer.ACTION_ALLIN, 0),
            (ClientBase.BettingAnswer.ACTION_CALL, 0)
        ]
        can_raise = current_bet + remaining_chips > minimum_to_raise_to
        bet = 10 + minimum_to_raise_to \
        if current_bet + remaining_chips + 10 > minimum_to_raise_to \
        else minimum_to_raise_to
        if can_raise: possible_actions.append((ClientBase.BettingAnswer.ACTION_RAISE, bet))

        # Evaluate actions
        prob_of_action = [(self.model.predict_proba(self.get_feature(action))[0][1], action, value) \
            for action, value in possible_actions]
        prob, best_action, value = max(prob_of_action, key=lambda x:x[0])
        print('prob', prob, 'best_action', best_action, 'value', value)

        # Inform agent of what we do
        switch = {
            ClientBase.BettingAnswer.ACTION_FOLD:self.foldAction,
            ClientBase.BettingAnswer.ACTION_CALL:self.callAction, 
            ClientBase.BettingAnswer.ACTION_ALLIN:self.allinAction,
            ClientBase.BettingAnswer.ACTION_RAISE:self.raiseAction
        }
        args={'_maximumBet':max_bet, '_playersCurrentBet':current_bet}
        switch[best_action](bet=bet, **args)
        self.players[self.name]['action'].append(best_action) #FIXME: ugly hotfix

        # Inform server
        if best_action == ClientBase.BettingAnswer.ACTION_RAISE:
            return (best_action, bet)
        return best_action

    def queryCardsToThrow(self, hand:list):
        "Strategy to throw cards. Aim is to throw when odds entailed from rank is worse than 20%"
        hand_strength = self.hand2Strength(hand)
        hand = hand[:5] # in case server sends extra gifts
        rank2int = {rank:i for i,rank in enumerate('123456789TJQKA')}
        hand.sort(key=lambda x:rank2int[x[0]], reverse=True) # sort on card rank
        slice2str = lambda x: ' '.join(x)
        if hand_strength < 3325: # if two pair or better
            return ' ' # top 8% is good enough
        elif hand_strength < 6185: # if pair
            index_of_pair = [index for index, (c1, c2) in enumerate(zip(hand[:-1], hand[1:])) if c1 == c2]
            if len(index_of_pair)==0: return slice2str(hand[1:]) # Hotfix for BUG: no pair found
            else: index_of_pair = index_of_pair[0]
            hand_copy = copy(hand)
            del hand_copy[index_of_pair:index_of_pair+1] # remove pair from cards to throw
            return slice2str(hand_copy[1:]) # worst 2 cards
        return slice2str(hand[1:]) # worst 4 cards
        
    def get_feature(self, next_action:str) -> List[int]:
        feature = [self.hand2Strength(self.CurrentHand)]
        chips = [self.Chips]
        actions = self.players[self.name]['action'][-1:]+['Player_'+next_action]
        playerCopy = deepcopy(self.players)
        del playerCopy[self.name]

        for info in playerCopy.values():
            chips.append(info['chips'])
            actions.extend(info['action'][-2:])
        feature.extend(chips)
        feature.extend(actions) 
        feature = ml.preprocess_row(feature, process=self.processes, args=self.args)
        return [feature]

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
            #1: ClientBase.BettingAnswer.ACTION_ALLIN,
        }.get(random.randint(0, 1), canOpen())

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
    
    