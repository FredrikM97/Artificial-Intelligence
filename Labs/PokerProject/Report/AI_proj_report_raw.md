## Abstract:

[summarise everything]

## Intorduction:

Games without exact solutions are common ways to learn machine learning. In this project we'll making a crude machine learning based agent for five card poker. In short, five card poker is like texas hold em but with five cards on hand and no cards on the board. All players get a hand, place some bets based on their perceptions, hands are shown and the winner takes the pot. For a more detailed description see the PEAS description in the method section. 

[What types of agent and AI methods can be applied?]
-Hidden information excludes all informed search algorithms. Randomness from hand excludes all exact solutions. This leaves us with:
-Uninformed search like bfs but with probability
-Statistics driven solution like ml
-Reflex agent that accounts for probabilities
-[Think i missed some. Double check this]
As with all opponent based games one can combine an opponent model with recursion to enhance the performance but due to the randomness in poker the recursion mustn't be to deep or it will reduce the agent to random actions.

[Are any relevant work being applied to this problem? / what are your references? Explain theories]

## Method:
[pick method from introduction and explain the parameters to said method]

-PEAS description
"PEAS stands for Performance, Environment, Actuators, and Sensors"
Performance:
	[Talk about metrics here]

Enviroment:
Five card poker conatins a set of objects, mechanics and a flow. 

	Objects: serve as achor points for actuators. Could aslo be seen as namespaces
		Chips: A players currency. when it runs out the player loses
		Cards: The building block of hands. Has rank and colour
		Hands: A combination of 5 cards. Given to the player by the game
		The pot: The accumulated bets from all players. 
		Player: The player/agent playing the game. The player owns chips
	Mechanics: These are operations/actuators belonging to game objects
		Chips machanics:
			-match: 
				Means matching the highest current bet
			-raise:
				Raising means increasing ones bet over the highest current bet which is turn forces all other players to respond. A raise must be equal to or greater than the previous raise, this is to prevent players from stalling the game.
		Cards machanics:
			-Display: cards can be made visible
			-Compare: cards can be compared by both rank and colour
		Hands machanics:
			-Discard: The act of throwing one or more cards which then gets replaced. This action can be seen by all players
			-Display: hands can be made visible
			-Compare: 
				[*insert short/clean explaination here*]
	Flow: The operations performed by the game itself. These can be called in any state machine fashion but in this case they are simply called in order.
		1.Ante
		2.The first betting round is made.
		3.If any players remain in the game, then each player can choose to change cards.
		4.The second betting round is made.
		5.Showdown, where the player hands are compared and the winner(s) will receive the pot (or part of the pot, in case of multiple winners).

Actuators: mechanics that belong to the player
	Open: Performes the raise actuator from chip without setting the minimum raise.
	Call: Trigger match actuator from chip
	Check: Also triggers chips match actuator
	Raise: Bound to chips raise actuator
	Fold: This actuator is unique for the player. It sets the agent state to folded meaning that the agent will not be affected by the game flow until the start of next round.
	All-in: Raise equal to the players chips.

Sensors:
	[our feature vector]
	
-xPeke behavior

## Experiment and tournament result

-"What have you observed when playing against a random agent or any agent you have developed?" Server drops, we observed server drops. The f do we write here?
-"Does the result match your expectations?" Had no expectation and was still let down.
-"Observation from the tournament" What tournament

Observations:
During the course of the project, several problems were observed. This includes drop from the server and information did not arrive as expected. This meant that the agents lost the connection to the server and were kicked for incorrect response or lack of response. The messages could come up empty "[]" or with multiple messages in one which caused major learning problems.
After a number of attempts, the idea was abandoned to try to solve the problem and tried to extract the data as well as it could to create a model of the game. Because of the quality of the data from the agents who came up with the project description, it was decided that being in the competition would not give a good idea of ​​how the model is constructed.

Without input data, it is not possible to create a model, so it is no surprise that the model does not work to the extent that would be considered arbitrary. Currently there are 2889 data points to train on, of which 1968 data points are unusable

## Conclusion

[Conclusion is just abstract in reverse. Change my mind]