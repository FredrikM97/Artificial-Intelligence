__author__ = 'fyt'

import socket
import random
import ClientBase

class Agent:
    def __init__(self, name, hand):
        self.name = name
        self.Chips = 0
        self.CurrentHand = hand
        self.Ante = 0
        self.playersCurrentBet = 0

    def queryOpenAction(self, minimumPotAfterOpen, playersCurrentBet, playersRemainingChips):
        '''
        * Called during the betting phases of the game when the player needs to decide what open
        * action to choose.
        '''
        raise NotImplementedError

    def queryCallRaiseAction(self, maximumBet, minimumAmountToRaiseTo, playersCurrentBet, playersRemainingChips):
        raise NotImplementedError

    def queryCardsToThrow(self, _hand):
        raise NotImplementedError

class RandomAgent(Agent):
    def __init__(self, name="Random", hand=[], ip='127.0.0.1', port=5000):
        Agent.__init__(self, name, hand)
        # IP address and port
        self.IP = ip
        self.PORT = port
        self.BUFFER_SIZE = 1024

    '''
    * Called during the betting phases of the game when the player needs to decide what open
    * action to choose.
    '''
    def queryOpenAction(self, _minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
        print("Player requested to choose an opening action.")
       
        def openAction():    
            if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
                #return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
                return ClientBase.BettingAnswer.ACTION_OPEN,  (random.randint(0, 10) + _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else _minimumPotAfterOpen
            else:
                return ClientBase.BettingAnswer.ACTION_CHECK

        return {
            0: ClientBase.BettingAnswer.ACTION_CHECK,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
        }.get(random.randint(0, 2), openAction())

   
    '''
    * Called during the betting phases of the game when the player needs to decide what call/raise
    * action to choose.
    '''
    def queryCallRaiseAction(self, _maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
        print("Player requested to choose a call/raise action.")

        def callRaise():
            # Random Open Action
            if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
                return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
            else:
                return ClientBase.BettingAnswer.ACTION_FOLD
    
        return {
            0: ClientBase.BettingAnswer.ACTION_FOLD,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
            2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
        }.get(random.randint(0, 3), callRaise())

    '''
    * Strategy to throw cards
    '''
    def queryCardsToThrow(self, _hand):
        print("Requested information about what cards to throw")
        print(_hand)
        return _hand[random.randint(0,4)] + ' '

