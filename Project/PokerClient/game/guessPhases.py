'''
*****  Guess current phase of server *****
''' 
    
def guessPhase(self,agent,RequestType):
    "Try to figure out which phase the server is in"
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
    while RequestType not in phase2set[self.phase] and RequestType not in phase2set[self.previousPhase()]:
        self.nextPhase()
        if self.hawkeye:
            print("Request:", RequestType, 'Agent phase:', self.phase)
def nextPhase(self):
    self.phaseIndex += 1
    self.phaseIndex %= len(self.gameFlow)
    self.phase = self.gameFlow[self.phaseIndex]
def previousPhase(self):
    prevPhaseIndex = self.phaseIndex + len(self.gameFlow)-1
    prevPhaseIndex %= len(self.gameFlow)
    return self.gameFlow[prevPhaseIndex]

def guessAction(self, msg, agent=None, MsgFractions=[], **kwarg):
    # Do action based on phase
    # Is this an action phase?
    if self.phase == 'info': # wrong phase
        self.nextPhase()
        print('Wrong phase!!')

    agent = self.agent if agent is None else agent # use local agent if none
    
    phase2action={
        'info':lambda *arg,**kwarg:None, 
        'open':self.handle_Open, 
        'betting':self.handle_Call_or_Raise,
        'draw':self.handle_Draw
    }
    #TODO: do the all-in case
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
def hourglass(self, *args, **kwargs):
    global RESPONSE_DELAY

    # if timer is already started: stop it
    if self.response_thread.is_alive():
        self.response_thread.cancel()
        self.response_thread.join()

    # Make new timer
    t = Timer(RESPONSE_DELAY, self.guessAction, args=args, kwargs=kwargs)
    t.setDaemon(True)
    t.start()
    self.response_thread = t
