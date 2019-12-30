import socket
import random
import ClientBase

class Agent:
    def __init__(self, name):
        self.name = name
        self.Chips = 0
        self.CurrentBet = 0
        self.Ante = 0
        self.CurrentHand = []
        self.maxBet = 1
        self.minRaise = 1
        self.gameData = [] # All info of opponents actions

    '''
    * Called during the betting phases of the game when the player needs to decide what open
    * action to choose.
    '''
    def queryOpenAction(self, minimumPotAfterOpen, playersCurrentBet, playersRemainingChips):
        raise NotImplementedError
   
    '''
    * Called during the betting phases of the game when the player needs to decide what call/raise
    * action to choose.
    '''
    def queryCallRaiseAction(self, maximumBet, minimumAmountToRaiseTo, playersCurrentBet, playersRemainingChips):
        raise NotImplementedError

    '''
    * Strategy to throw cards
    '''
    def queryCardsToThrow(self, _hand):
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
        

class RandomAgent(Agent):
    def __init__(self, name="Random", hand=[], ip='127.0.0.1', port=5000):
        Agent.__init__(self, name)
        # IP address and port
        self.IP = ip
        self.PORT = port
        self.BUFFER_SIZE = 1024

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

