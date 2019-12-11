'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoResult(msg, **kwargs):
    #_nrTimeRaised = 0
    _playerName, _round, _chips, *_ = msg
    print(f'{_playerName} lasted {_round} rounds. Final chips: {_chips}')

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(msg, **kwargs):
    #_nrTimeRaised = 0
    _round, *_ = msg
    print('Starting Round: ' + _round )

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver(*_, **kwargs):
    print('The game is over.')

'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(msg, **kwargs):
    _playerName, _openBet, *_ = msg
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(msg, **kwargs):
    _playerName, *_ = msg
    print("Player "+ _playerName +" checked.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(msg, **kwargs):
    _playerName, *_ = msg
    print("Player "+_playerName +" called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(msg, **kwargs):
    _playerName, *_ = msg
    print("Player "+ _playerName +" folded.")

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(msg, **kwargs):
    _playerName, _chips, *_ = msg
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundUndisputedWin(msg, **kwargs):
    _playerName, _winAmount, *_ = msg
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(msg, **kwargs):
    _playerName, _allInChipCount, *_ = msg
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(msg, **kwargs):
    _playerName, _winAmount, *_ = msg
    print("Player "+ _playerName +" won " + _winAmount + " chips.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(msg, **kwargs):
    _playerName, _hand, *_ = msg
    print("Player "+ _playerName +" hand " + str(_hand))

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(msg, **kwargs):
    _playerName, _cardCount, *_ = msg
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(msg, **kwargs):
    _playerName, _amountRaisedTo, *_ = msg
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(msg, **kwargs):
    _ante, *_ = msg
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(msg, **kwargs):
    _playerName, _forcedBet, *_ = msg
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")
