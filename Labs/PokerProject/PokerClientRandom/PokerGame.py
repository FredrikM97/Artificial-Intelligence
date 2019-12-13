__author__ = 'Fredrik M, Jesper H'
__version__= 'Python: 3.7.4, Program: 1.0'

import socket
import random
import ClientBase
import time
import sys, os
from threading import Thread

from Client import RandomAgent
from game.serverInfo import * 


def main():
    print("Starting game.. Waiting for server")
    # Make client1
    myClient1 = client(RandomAgent('Subject1.0', ip='127.0.0.1',port=5000), True)
    t1 = Thread(target=myClient1.run)

    # Make client2
    myClient2 = client(RandomAgent('Subject2.0', ip='127.0.0.2',port=5000), False)
    t2 = Thread(target=myClient2.run)
    
    # Make client3
    myClient3 = client(RandomAgent('Subject3.0', ip='127.0.0.3',port=5000), False)
    t3 = Thread(target=myClient3.run)
    
    t1.start()
    t2.start()
    t3.start()

class client:
    def __init__(self, agent, hawkeye):
        # Connect agent
        self.agent = agent # Import the agent info
        self.hawkeye = hawkeye
        self.phase = 'info'

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5.0)
        self.s.connect((self.agent.IP, self.agent.PORT))

        # Declare constants
        self.SIGNAL_ALIVE = '==================ALIVE======================' 
        self.iMsg = 0
        self.gameFlow = ['info','open','betting','draw','betting']
        self.phaseIndex = 0

    '''
    ***** Get data from server *****
    '''    
    # Get how much chips agent has, or print opponents chips
    def handle_Chips(self, *_, agent=None, MsgFractions=[], **kwargs):
        if MsgFractions[0] == agent.name:
            agent.Chips = int(MsgFractions[1])
        else:
            infoPlayerChips(MsgFractions, **kwargs) 

    # Get Ante to agent, and print it
    def handle_Ante_Changed(self, *_, agent=None, MsgFractions=[], **kwargs):
        agent.Ante = int(MsgFractions[0])
        infoAnteChanged(MsgFractions, **kwargs)

    # Get Raised to agent, and print it
    def handle_Info_Raise(self, *_, agent=None, MsgFractions=[], **kwargs):
        oldmax = agent.maxBet
        agent.maxBet = int(MsgFractions[1])
        agent.minRaise = agent.maxBet - oldmax
        infoPlayerRise(MsgFractions, **kwargs)

    # Get open bet to agent, and print it
    def handle_Info_Player_Open(self, *_, agent=None, MsgFractions=[], **kwargs):
        agent.maxBet = int(MsgFractions[1])
        agent.minRaise = 1
        infoPlayerOpen(MsgFractions, **kwargs)

    # Give hand to agent
    def handle_Cards(self, *_, agent=None, MsgFractions=[], **kwargs):
        #infoCardsInHand(MsgFractions) # show info for hands
        agent.CurrentHand = []
        for ielem in MsgFractions: # never go full retard
            agent.CurrentHand.append(ielem)
        infoPlayerHand((agent.name, *MsgFractions), **kwargs)
        #print('CurrentHand>', agent.CurrentHand)

    '''
    ***** ACTIONS to server *****
    '''    
    def send_but_working(self,string): # use this when doing python 3+
        print('Current phase:', self.phase, 'Message:',string)
        self.nextPhase()
        self.s.send(str.encode(string + '\n'))
        
    # Return agent name to Server
    def handle_name(self, *_, agent=None, MsgFractions=[], **kwargs):
        self.send_but_working('Name ' + agent.name)
        self.phase = 'info'
        self.phaseIndex = 0

    # Force a bet if agents turn
    def handle_Forced_Bet(self, *_, agent=None, MsgFractions=[], **kwargs):
        if MsgFractions[0] == agent.name:
            agent.CurrentBet += int(MsgFractions[1])
        else:
            infoForcedBet(MsgFractions, **kwargs)

    # Open bet at beginning depending on Agent
    def handle_Open(self, *_, agent=None, MsgFractions=[], **kwargs):
        intFractions = [int(Fraction) for Fraction in MsgFractions]
        # minimumPotAfterOpen, CurrentBet, playersRemainingChips = intFractions
        tmp = agent.queryOpenAction(*intFractions)

        # For check and All-in/ Open
        to_send = tmp if issubclass(tmp.__class__, str) else ' '.join([str(item) for item in tmp])
        print("Open:",to_send)
        self.send_but_working(to_send)
        
        print(f'{self.SIGNAL_ALIVE} \n {agent.name} Action: {tmp}')

    # Do a call or raise depending on Agent
    def handle_Call_or_Raise(self, *_, agent=None, MsgFractions=[], **kwargs):
        intFractions = [int(Fraction) for Fraction in MsgFractions]
        # maximumBet, minimumAmountToRaiseTo, CurrentBet, playersRemainingChips = intFractions
        tmp = agent.queryCallRaiseAction(*intFractions)

        # For fold, all-in, call / For raise
        to_send = tmp if issubclass(tmp.__class__,str) else ' '.join([str(item) for item in tmp])
        print("Call:",to_send)
        self.send_but_working(to_send)
        
        print(f'{self.SIGNAL_ALIVE} \n {agent.name} Action: {tmp}')

    # Throw agent hand   
    def handle_Draw(self, *_, agent=None, MsgFractions=[], **kwargs):
        discardCards = agent.queryCardsToThrow(agent.CurrentHand)
        self.send_but_working('Throws ' + discardCards)
        print(agent.name, 'Action:','Throws', discardCards)
    '''
    *****  Guess current phase of server *****
    ''' 
    # Try to figure out which phase
    def guessPhase(self,agent,RequestType):
        # black magic fuckery to save us from creating the sets every call
        if 'phase2set' not in self.guessPhase.__dict__:
            infoSet = {
                'Name?',
                'Chips',
                'Ante_Changed',
                'Forced_Bet',   
                'Cards',
                'Round',
                'Game_Over',
                'Player_Draw',
                'Round_Win_Undisputed',
                'Round_result',
                'Player_Hand',
                'Result',
                'unknown_action'
            }
            openSet = {
                'Open?',
                'Player_Open',
                'Player_Check',
                'Player_All-in',
                'unknown_action'
            }
            betttingSet = {
                'Call/Raise?',
                'Player_Raise',
                'Player_Call',
                'Player_Fold',
                'Player_All-in',
                'unknown_action'
            }

            drawSet = {
                'Draw?'
            }

            phase2set = {
                'info':infoSet, 
                'open':openSet, 
                'betting':betttingSet,
                'draw':drawSet
            }
            self.guessPhase.__dict__.update({'phase2set':phase2set})
        else:
            phase2set = self.guessPhase.__dict__['phase2set']

        # While not in current -> next
        print('Type:',RequestType, "Phasor:",self.phase)
        while RequestType not in phase2set[self.phase]:
            self.nextPhase()
            if self.hawkeye:
                print("Request:", RequestType, 'Agent phase:', self.phase)

    
    def nextPhase(self):
        self.phaseIndex += 1
        self.phaseIndex %= len(self.gameFlow)
        self.phase = self.gameFlow[self.phaseIndex]

    # Do action based on phase
    def guessAction(self, msg, agent=None, MsgFractions=[], **kwarg):
        agent = self.agent if agent is None else agent # use local agent if none
        
        phase2action={
            'info':lambda *arg,**kwarg:None, 
            'open':self.handle_Open, 
            'betting':self.handle_Call_or_Raise,
            'draw':self.handle_Draw
        }
        #TODO: do the all in case
        minimumPotAfterOpen = agent.Ante * 5 # TODO: reeee member it's 5 as in 5 players
        CurrentBet = agent.CurrentBet
        maximumBet = agent.maxBet
        minimumAmountToRaiseTo = maximumBet + agent.minRaise
        playersRemainingChips = agent.Chips

        phase2msg = {
            'info':[], 
            'open':[minimumPotAfterOpen, CurrentBet, playersRemainingChips], 
            'betting':[maximumBet, minimumAmountToRaiseTo, CurrentBet, playersRemainingChips],
            'draw':[]
        }

        phase2action[self.phase](agent=agent, MsgFractions=phase2msg[self.phase], **kwarg)
        
    '''
    ***** Run *****
    ''' 
    def run(self):
        infoTablets = {
            'Name?':self.handle_name,
            'Chips':self.handle_Chips,
            'Ante_Changed':self.handle_Ante_Changed,
            'Forced_Bet':self.handle_Forced_Bet,
            'Open?':self.handle_Open,
            'Call/Raise?':self.handle_Call_or_Raise,
            'Cards':self.handle_Cards,
            'Draw?':self.handle_Draw,
            'Round':infoNewRound,
            'Game_Over':infoGameOver,
            'Player_Open':self.handle_Info_Player_Open,
            'Player_Check':infoPlayerCheck,
            'Player_Raise':self.handle_Info_Raise,
            'Player_Call':infoPlayerCall,
            'Player_Fold':infoPlayerFold,
            'Player_All-in':infoPlayerAllIn,
            'Player_Draw':infoPlayerDraw,
            'Round_Win_Undisputed':infoRoundUndisputedWin,
            'Round_result':infoRoundResult,
            'Player_Hand':infoPlayerHand,
            'Result':infoResult,
            'unknown_action':self.guessAction
        }

        while True:
            try:
                data = self.s.recv(self.agent.BUFFER_SIZE) # Get data
                if not data: break
                MsgFractions = data.split() # split string into fraction

                if len(MsgFractions) == 0: MsgFractions = [b'unknown_action']

                MsgFractions = [msg.decode('utf-8') for msg in MsgFractions] # Get Request type
                RequestType, *MsgFractions = MsgFractions
                self.guessPhase(self.agent,RequestType)
                
                self.iMsg += 1  # No. of Msg

                kwarg = {
                    'agent':self.agent, 
                    'MsgFractions':MsgFractions,
                    'verbose':self.hawkeye}

                infoTablets[RequestType](MsgFractions, **kwarg)
                    
            except socket.timeout:
                #sys.stdout = sys.__stdout__ # Turn on prints
                print(f'{self.agent.name} has commited soduko')
                break

        self.s.close()
        
if __name__ == "__main__":
    main()

'''
TODO:
* Add value check of hand ?que?
* What to bet, Fold, call. random
* If to throw cards. also random
* Threading working properly, std out is disabled by other threads while thread 1 runs
'''