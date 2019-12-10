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
infoAgent = RandomAgent()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((infoAgent.IP, infoAgent.PORT))

infoTablets = {
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

while True:

    try:
        # Get data
        data = s.recv(infoAgent.BUFFER_SIZE)
        
        # split string into fraction
        MsgFractions = data.split()

        # Check if message is empty
        if len(MsgFractions) == 0:
            continue

        # No. of Msg
        iMsg = iMsg + 1
        # print('MsgFractions', data)

        # Get Request type
        RequestType = MsgFractions[0]
        #print('CMD', RequestType)


        # "Name?"
        # /** Sent from server to clients before the game starts. */
        if RequestType == 'Name?': # if Server request for name
            s.send('Name ' + infoAgent.PlayerName + "\n")

        # "Chips"
        #/** Sent from server to clients when the server informs the players how many chips a player has.
        # * Append space, the players name, space and the amount of chips after this string. Separate the words by space. */
        elif RequestType == 'Chips': # if Server remind player chips cumber
            if MsgFractions[1] == infoAgent.PlayerName:
                infoAgent.Chips = int(MsgFractions[2])
        
            else:
                infoPlayerChips(MsgFractions[1], MsgFractions[2]) #TODO
            
        #"Ante_Changed"
        # /** Sent from server to clients when the server informs the players that the ante has changed.
        # * Append space and the value of the ante after this string. */
        elif RequestType == 'Ante_Changed': # if ante is changed
            infoAgent.Ante = int(MsgFractions[1])
            infoAnteChanged(MsgFractions[1])#TODO

        #"Forced_Bet"
        # /** Sent from server to clients when the server informs the players that a player has made a forced bet (the ante).
        # * Append the players name and the bet value after this string. Separate the words by space. */
        elif RequestType == 'Forced_Bet': # Notice force bet
            if MsgFractions[1] == infoAgent.PlayerName:
                infoAgent.playersCurrentBet = infoAgent.playersCurrentBet + int(MsgFractions[2])
            else:
                infoForcedBet(MsgFractions[1], MsgFractions[2])#TODO

        # "Open?"
        #/** Sent from server to clients as information when a player opens.
        # * Append the players name and the total amount of chips the player has put into into the pot after this string.
        # * Separate the words by space. */
        elif RequestType == 'Open?':
            # sleep for 3 s... You can remove it...
            minimumPotAfterOpen = int(MsgFractions[1])
            playersCurrentBet = int(MsgFractions[2])
            playerRemainingChips = int(MsgFractions[3])

            tmp = queryOpenAction(minimumPotAfterOpen, playersCurrentBet, playerRemainingChips)

            if isinstance( tmp, str ): # For check and All-in
                s.send(tmp + "\n")
            elif len(tmp) == 2: # For open
                s.send(tmp[0] + ' ' + str(tmp[1]) + " \n")

            print(SIGNAL_ALIVE)
            print(infoAgent.PlayerName + 'Action>', tmp)

        elif RequestType == 'Call/Raise?':
            maximumBet = int(MsgFractions[1])
            minimumAmountToRaiseTo = int(MsgFractions[2])
            playersCurrentBet = int(MsgFractions[3])
            playersRemainingChips = int(MsgFractions[4])

            tmp = queryCallRaiseAction(maximumBet, minimumAmountToRaiseTo, playersCurrentBet, playersRemainingChips)

            if isinstance( tmp, str ): # For fold, all-in, call
                s.send(tmp + "\n")
            elif len(tmp) == 2: # For raise
                s.send(tmp[0] + ' ' + str(tmp[1]) + " \n")

            print(SIGNAL_ALIVE)
            print(infoAgent.PlayerName + 'Action>',  tmp)
            
        elif RequestType == 'Cards': # Get Cards
            #infoCardsInHand(MsgFractions) # show info for hands
            infoAgent.CurrentHand = []
            for ielem in range(1,6): # 1 based indexing is required...
                infoAgent.CurrentHand.append(MsgFractions[ielem])
            infoPlayerHand(infoAgent.PlayerName, infoAgent.CurrentHand)
            #print('CurrentHand>', infoAgent.CurrentHand)
        elif RequestType == 'Draw?':
            discardCards = queryCardsToThrow(infoAgent.CurrentHand)
            s.send('Throws ' + discardCards + "\n")

            print(infoAgent.PlayerName + ' Action>' + 'Throws ' + discardCards)

        else:
            infoTablets[RequestType](MsgFractions[1], MsgFractions[2])
            
    except socket.timeout:
        break

s.close()









