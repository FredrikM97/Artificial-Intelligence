__author__ = 'fyt'

import socket
import random
import ClientBase
import time

from Client import RandomAgent
from game.serverInfo import * 

iMsg = 0
SIGNAL_ALIVE = '==================ALIVE======================'

# Import the agent info
agent = RandomAgent('Why no namies')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((agent.IP, agent.PORT))

def send_but_working(string): # use this when doing python 3+
    s.send(str.encode(string + '\n'))

def handle_name(*_, agent=None, **kwargs):
    send_but_working('Name ' + agent.name)
 
def handle_Chips(agent=None, MsgFractions=None, *_, **kwargs):
    if MsgFractions[1] == agent.name:
        agent.Chips = int(MsgFractions[2])
    else:
        infoPlayerChips(MsgFractions[1], MsgFractions[2]) #TODO

def handle_Ante_Changed(agent=None, *_, **kwargs):
    agent.Ante = int(MsgFractions[1])
    infoAnteChanged(MsgFractions[1])#TODO

def handle_Forced_Bet(agent=None, MsgFractions=None, *_, **kwargs):
    if MsgFractions[1] == agent.name:
        agent.playersCurrentBet = agent.playersCurrentBet + int(MsgFractions[2])
    else:
        infoForcedBet(MsgFractions[1], MsgFractions[2])#TODO
        
def handle_Open(agent=None, MsgFractions=None, *_, **kwargs):
    minimumPotAfterOpen = int(MsgFractions[1])
    playersCurrentBet = int(MsgFractions[2])
    playerRemainingChips = int(MsgFractions[3])

    tmp = agent.queryOpenAction(minimumPotAfterOpen, playersCurrentBet, playerRemainingChips)
    
    if isinstance( tmp, str ): # For check and All-in
        send_but_working(tmp)
    elif len(tmp) == 2: # For open
        send_but_working(tmp[0] + ' ' + str(tmp[1]))

    print(SIGNAL_ALIVE)
    print(agent.name + 'Action>', tmp)

def handle_Call_or_Raise(agent=None, MsgFractions=None, *_, **kwargs):
    maximumBet = int(MsgFractions[1])
    minimumAmountToRaiseTo = int(MsgFractions[2])
    playersCurrentBet = int(MsgFractions[3])
    playersRemainingChips = int(MsgFractions[4])
    
    tmp = agent.queryCallRaiseAction(maximumBet, minimumAmountToRaiseTo, playersCurrentBet, playersRemainingChips)
    
    if isinstance( tmp, str ): # For fold, all-in, call
        send_but_working(tmp)
    elif len(tmp) == 2: # For raise
        send_but_working(tmp[0] + ' ' + str(tmp[1]))

    print(SIGNAL_ALIVE)
    print(agent.name + 'Action>',  tmp)
            
def handle_Cards(agent=None, MsgFractions=None, *_, **kwargs):
    #infoCardsInHand(MsgFractions) # show info for hands
    agent.CurrentHand = []
    for ielem in range(1,6): # 1 based indexing is required...
        agent.CurrentHand.append(MsgFractions[ielem])
    infoPlayerHand(agent.name, agent.CurrentHand)
    #print('CurrentHand>', agent.CurrentHand)
      
def handle_Draw(agent=None, *_, **kwargs):
    discardCards = agent.queryCardsToThrow(agent.CurrentHand)
    send_but_working('Throws ' + discardCards)
    print(agent.name + ' Action>' + 'Throws ' + discardCards)

infoTablets = {
    'Name?':handle_name,
    'Chips':handle_Chips,
    'Ante_Changed':handle_Ante_Changed,
    'Forced_Bet':handle_Forced_Bet,
    'Open':handle_Open,
    'Call_or_Raise':handle_Call_or_Raise,
    'Cards':handle_Cards,
    'Draw':handle_Draw,
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
    'Player_Hand':infoPlayerHand
}
print("Starting game.. Waiting for server")
while True:
    try:
        # Get data
        data = s.recv(agent.BUFFER_SIZE)
        
        # split string into fraction
        MsgFractions = data.split()

        # Check if message is empty
        if len(MsgFractions) == 0:
            continue

        # No. of Msg
        iMsg = iMsg + 1
        # print('MsgFractions', data)

        # Get Request type
        MsgFractions = [msg.decode('utf-8') for msg in MsgFractions]
        RequestType, *MsgFractions = MsgFractions
        #print('CMD', RequestType)

        kwarg = {
            'agent':agent, 
            'MsgFractions':MsgFractions,
            }
        print(RequestType,MsgFractions)
        infoTablets[RequestType](MsgFractions, **kwarg)
            
    except socket.timeout:
        break

s.close()



