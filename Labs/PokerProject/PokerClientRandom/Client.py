__author__ = 'fyt'

import socket
import random
import ClientBase

class RandomAgent():
    def __init__(self, name="Random", hand=[]):
        self.PlayerName = name
        self.Chips = 0
        self.CurrentHand = hand
        self.Ante = 0
        self.playersCurrentBet = 0

        # IP address and port
        self.IP = '127.0.0.1'
        self.PORT = 5000
        self.BUFFER_SIZE = 1024

    '''
    * Gets the name of the player.
    * @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
    '''
    def queryPlayerName(self):
        return self.PlayerName

    '''
    * Called during the betting phases of the game when the player needs to decide what open
    * action to choose.
    '''

    def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
        print("Player requested to choose an opening action.")
       
        def openAction(self):    
            if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
                #return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
                return ClientBase.BettingAnswer.ACTION_OPEN,  (random.randint(0, 10) + _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else _minimumPotAfterOpen
            else:
                return ClientBase.BettingAnswer.ACTION_CHECK

        return {
            0: ClientBase.BettingAnswer.ACTION_CHECK,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
        }.get(random.randint(0, 2), self.openAction())

   
    '''
    * Called during the betting phases of the game when the player needs to decide what call/raise
    * action to choose.
    '''
    
    def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
        print("Player requested to choose a call/raise action.")

        def callRaise(self):
            # Random Open Action
            if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
                return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
            else:
                return ClientBase.BettingAnswer.ACTION_FOLD
                
        return {
            0: ClientBase.BettingAnswer.ACTION_FOLD,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
            2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
        }.get(random.randint(0, 3), self.agent.callRaise())

    '''
    * Strategy to throw cards
    '''
    def queryCardsToThrow(_hand):
        print("Requested information about what cards to throw")
        print(_hand)
        return _hand[random.randint(0,4)] + ' '

