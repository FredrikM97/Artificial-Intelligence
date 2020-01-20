__author__ = 'Fredrik M, Jesper H'
__version__= 'Python: 3.7.4, Program: 1.0'

import socket
import random
import ClientBase
import time
import sys, os
from threading import Thread, Timer
from itertools import repeat

from Client import RandomAgent, ml_agent
from game.serverInfo import * 

RESPONSE_DELAY = 0.5 # In seconds

def main():
    
    agents = [
        ml_agent(name='Synthesis_1'),
        ml_agent(name='Synthesis_2'),
        ml_agent(name='Synthesis_3'),
        ml_agent(name='Synthesis_4'),
        ml_agent(name='Synthesis_5'),
    ]
    observe = [True]+[*repeat(False,len(agents)-1)]
    print("Starting game.. Waiting for server")

    for agent, eye in zip(agents, observe):
        c = client(agent, hawkeye=eye)
        t = Thread(target=c.run)
        t.start()
        
class client:
    def __init__(self, agent, ip='localhost', port=5000, hawkeye=False):
        # Connect agent
        self.agent = agent # Import the agent info
        self.hawkeye = hawkeye
        self.phase = 'info'
        self.BUFFER_SIZE = 1024

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(8.0)
        self.s.connect((ip, port))

        # Declare constants
        self.SIGNAL_ALIVE = '==================ALIVE======================' 
        self.iMsg = 0
        self.gameFlow = ['info','open','betting','draw','betting']
        self.phaseIndex = 0
        self.response_thread = Timer(RESPONSE_DELAY, lambda:None)

    '''
    ***** Get data from server *****
    '''    
    # Get how much chips agent has, or print opponents chips
    def handle_Chips_Changed(self, *_, agent=None, MsgFractions=[], **kwargs):
        if MsgFractions[0] == agent.name:
            agent.Chips = int(MsgFractions[1])
        else:
            infoPlayerChips(MsgFractions,agent=agent, **kwargs) 

    # Get Ante to agent, and print it
    def handle_Ante_Changed(self, *_, agent=None, MsgFractions=[], **kwargs):
        agent.Ante = int(MsgFractions[0])
        infoAnteChanged(MsgFractions, **kwargs)

    # Get Raised to agent, and print it
    def handle_Raise_Changed(self, *_, agent=None, MsgFractions=[], **kwargs):
        oldmax = agent.maxBet
        agent.maxBet = int(MsgFractions[1])
        agent.minRaise = agent.maxBet - oldmax
        infoPlayerRise(MsgFractions, agent=agent,**kwargs)

    # Get open bet to agent, and print it
    def handle_Player_Open_Changed(self, *_, agent=None, MsgFractions=[], **kwargs):
        agent.maxBet = int(MsgFractions[1])
        agent.minRaise = 1
        infoPlayerOpen(MsgFractions, agent=agent, **kwargs)

    # Give hand to agent
    def handle_Cards_Changed(self, *_, agent=None, MsgFractions=[], **kwargs):
        agent.CurrentHand = []
        for ielem in MsgFractions: # never go full retard
            agent.CurrentHand.append(ielem)
        infoPlayerHand((agent.name, *MsgFractions), agent=agent, **kwargs)

    '''
    ***** ACTIONS to server *****
    '''    
    def send_but_working(self,string): # use this when doing python 3+
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
        self.send_but_working(to_send)
        

    # Do a call or raise depending on Agent
    def handle_Call_or_Raise(self, *_, agent=None, MsgFractions=[], **kwargs):
        intFractions = [int(Fraction) for Fraction in MsgFractions]
        # maximumBet, minimumAmountToRaiseTo, CurrentBet, playersRemainingChips = intFractions
        tmp = agent.queryCallRaiseAction(*intFractions)

        # For fold, all-in, call / For raise
        to_send = tmp if issubclass(tmp.__class__,str) else ' '.join([str(item) for item in tmp])
        self.send_but_working(to_send)
        
    # Throw agent hand   
    def handle_Draw(self, *_, agent=None, MsgFractions=[], **kwargs):
        discardCards = agent.queryCardsToThrow(agent.CurrentHand)
        self.send_but_working('Throws ' + discardCards)
        
    '''
    ***** Run *****
    ''' 
    def run(self):
        infoTablets = {
            'Name?':self.handle_name,
            'Chips':self.handle_Chips_Changed,
            'Ante_Changed':self.handle_Ante_Changed,
            'Forced_Bet':self.handle_Forced_Bet,
            'Open?':self.handle_Open,
            'Call/Raise?':self.handle_Call_or_Raise,
            'Cards':self.handle_Cards_Changed,
            'Draw?':self.handle_Draw,
            'Round':infoNewRound,
            'Player_Open':self.handle_Player_Open_Changed,
            'Player_Check':infoPlayerCheck, 
            'Player_Raise':self.handle_Raise_Changed, 
            'Player_Call':infoPlayerCall, 
            'Player_Fold':infoPlayerFold,
            'Player_All-in':infoPlayerAllIn, 
            'Player_Hand':infoPlayerHand, 
            'Player_Draw':infoPlayerDraw, 
            'Round_Win_Undisputed':infoRoundUndisputedWin, 
            'Round_result':infoRoundResult,
            'Result':infoResult,
            'Game_Over':infoGameOver, 
            'unknown_action':lambda *a,**kw:None
        }

        msg2len = { # Maps message to excepted length of message
            'Name?':0,
            'Chips':2,
            'Ante_Changed':1,
            'Forced_Bet':2,
            'Open?':3,
            'Call/Raise?':4,
            'Cards':5,
            'Draw?':0,
            'Round':1, 
            'Player_Open':2, 
            'Player_Check':1,
            'Player_Raise':2,
            'Player_Call':1, 
            'Player_Fold':1,
            'Player_All-in':2, 
            'Player_Hand':6, 
            'Player_Draw':2, 
            'Round_Win_Undisputed':2,
            'Round_result':2, 
            'Result':3,
            'Game_Over':0, 
            'unknown_action':0
        }

        nagle_buffer = []
        while True:
            try:
                data = self.s.recv(self.BUFFER_SIZE) # Get data
                if not data: break
                MsgFractions = data.split() # split string into fraction
                
                if len(MsgFractions) == 0: 
                    continue

                MsgFractions = [msg.decode('utf-8') for msg in MsgFractions] # Get Request type
                
                # Queue message and pick real message from queue
                nagle_buffer.extend(MsgFractions)
                
                #Empty buffer before receiving new messages
                while len(nagle_buffer):
                    RequestType = nagle_buffer.pop(0)
                    msg_len = msg2len[RequestType]
                    MsgFractions = nagle_buffer[:msg_len]
                    del nagle_buffer[:msg_len]

                    self.iMsg += 1  # No. of Msg

                    kwarg = {
                        'agent':self.agent, 
                        'MsgFractions':MsgFractions,
                        'verbose':self.hawkeye}

                    infoTablets[RequestType](MsgFractions, **kwarg)
                        
            except socket.timeout as evil:
                print(f'{self.agent.name} has commited soduko because {evil}')
                break
        if self.hawkeye:
            print(*self.agent.players.items(),sep='\n')
        self.s.close()
        
if __name__ == "__main__":
    main()