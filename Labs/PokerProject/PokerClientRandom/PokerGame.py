__author__ = 'Fredrik M, Jesper H'
__version__= 'Python: 3.7.4, Program: 1.0'

import socket
import random
import ClientBase
import time
from threading import Thread

from Client import RandomAgent
from game.serverInfo import * 

def main():
    # Make client1
    myClient1 = client(RandomAgent('Subject1.0', port=5000))
    t1 = Thread(target=myClient1.run)
    t1.start()

    # Make client2
    myClient2 = client(RandomAgent('Subject2.0', ip='127.0.0.2',port=5000))
    t2 = Thread(target=myClient2.run)
    t2.start()

class client:
    def __init__(self, agent):
        # Connect agent
        self.agent = agent # Import the agent info
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.agent.IP, self.agent.PORT))

        # Declare constants
        self.SIGNAL_ALIVE = '==================ALIVE======================' 
        self.iMsg = 0
        
    def send_but_working(self,string): # use this when doing python 3+
        self.s.send(str.encode(string + '\n'))

    # Return agent name to Server
    def handle_name(self, *_, agent=None, MsgFractions=[], **kwargs):
        self.send_but_working('Name ' + agent.name)
    
    # Get how much chips agent has, or print opponents chips
    def handle_Chips(self, *_, agent=None, MsgFractions=[], **kwargs):
        if MsgFractions[0] == agent.name:
            agent.Chips = int(MsgFractions[1])
        else:
            infoPlayerChips(MsgFractions) #TODO

    # Get Ante to agent, and print it
    def handle_Ante_Changed(self, *_, agent=None, MsgFractions=[], **kwargs):
        agent.Ante = int(MsgFractions[0])
        infoAnteChanged(MsgFractions)#TODO

    # Force a bet if agents turn
    def handle_Forced_Bet(self, *_, agent=None, MsgFractions=[], **kwargs):
        if MsgFractions[1] == agent.name:
            agent.playersCurrentBet = agent.playersCurrentBet + int(MsgFractions[1])
        else:
            infoForcedBet(MsgFractions)#TODO

    # Open bet at beginning depending on Agent
    def handle_Open(self, *_, agent=None, MsgFractions=[], **kwargs):
        minimumPotAfterOpen = int(MsgFractions[0])
        playersCurrentBet = int(MsgFractions[1])
        playerRemainingChips = int(MsgFractions[2])

        tmp = agent.queryOpenAction(minimumPotAfterOpen, playersCurrentBet, playerRemainingChips)
        
        if isinstance( tmp, str ): # For check and All-in
            self.send_but_working(tmp)
        elif len(tmp) == 2: # For open
            self.send_but_working(tmp[0] + ' ' + str(tmp[1]))

        print(self.SIGNAL_ALIVE)
        print(agent.name + 'Action>', tmp)

    # Do a call or raise depending on Agent
    def handle_Call_or_Raise(self, *_, agent=None, MsgFractions=[], **kwargs):
        maximumBet = int(MsgFractions[0])
        minimumAmountToRaiseTo = int(MsgFractions[1])
        playersCurrentBet = int(MsgFractions[2])
        playersRemainingChips = int(MsgFractions[3])
        
        tmp = agent.queryCallRaiseAction(maximumBet, minimumAmountToRaiseTo, playersCurrentBet, playersRemainingChips)
        
        if isinstance( tmp, str ): # For fold, all-in, call
            self.send_but_working(tmp)
        elif len(tmp) == 2: # For raise
            self.send_but_working(tmp[0] + ' ' + str(tmp[1]))

        print(self.SIGNAL_ALIVE)
        print(agent.name + 'Action>',  tmp)

    # Give hand to agent
    def handle_Cards(self, *_, agent=None, MsgFractions=[], **kwargs):
        #infoCardsInHand(MsgFractions) # show info for hands
        agent.CurrentHand = []
        for ielem in MsgFractions: # never go full retard
            agent.CurrentHand.append(ielem)
        infoPlayerHand(MsgFractions, **kwargs)
        #print('CurrentHand>', agent.CurrentHand)

    # Throw agent hand   
    def handle_Draw(self, *_, agent=None, MsgFractions=[], **kwargs):
        discardCards = agent.queryCardsToThrow(agent.CurrentHand)
        self.send_but_working('Throws ' + discardCards)
        print(agent.name + ' Action>' + 'Throws ' + discardCards)

    def run(self):
        infoTablets = {
            'Name?':self.handle_name,
            'Chips':self.handle_Chips,
            'Ante_Changed':self.handle_Ante_Changed,
            'Forced_Bet':self.handle_Forced_Bet,
            'Open?':self.handle_Open,
            'Call_or_Raise':self.handle_Call_or_Raise,
            'Cards':self.handle_Cards,
            'Draw':self.handle_Draw,
            'Round':infoNewRound,
            'Game_Over':infoGameOver,
            'Player_Open':infoPlayerOpen,
            'Player_Check':infoPlayerCheck,
            'Player_Raise':infoPlayerRise,
            'Player_Call':infoPlayerCall,
            'Player_Fold':infoPlayerFold,
            'Player_All-in':infoPlayerAllIn,
            'Player_Draw':infoPlayerDraw,
            'Round_Win_Undisputed':infoRoundUndisputedWin,
            'Round_result':infoRoundResult,
            'Player_Hand':infoPlayerHand,
            'Result':infoResult}

        print("Starting game.. Waiting for server")
        
        while True:
            try:
                data = self.s.recv(self.agent.BUFFER_SIZE) # Get data
                
                MsgFractions = data.split() # split string into fraction

                if len(MsgFractions) == 0: continue # Check if message is empty

                self.iMsg += 1  # No. of Msg
                # print('MsgFractions', data)
                
                MsgFractions = [msg.decode('utf-8') for msg in MsgFractions] # Get Request type
                RequestType, *MsgFractions = MsgFractions
                #print('CMD', RequestType)

                kwarg = {
                    'agent':self.agent, 
                    'MsgFractions':MsgFractions,
                    }
                #print(RequestType,MsgFractions)
                infoTablets[RequestType](MsgFractions, **kwarg)
                    
            except socket.timeout:
                break

        s.close()
        '''
        TODO:
        * Add value check of hand
        * What to bet, Fold, call
        * If to throw cards
        '''
if __name__ == "__main__":
    main()