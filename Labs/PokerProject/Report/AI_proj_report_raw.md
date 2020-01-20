## Abstract:
[summarise everything]

## Introduction:
Games without exact solutions are common ways to learn machine learning. In this project we'll making a crude machine learning based agent for five card poker. In short, five card poker is like texas hold em but with five cards on hand and no cards on the board. All players get a hand, place some bets based on their perceptions, hands are shown and the winner takes the pot. For a more detailed description see the PEAS description in the method section. 

[What types of agent and AI methods can be applied?]

There's more than one way to aproach this task of making a poker agent. A handful of solutions have been concidered but the set can be narrowed down by concidering the restrictions the game applies to our model. We have hidden information which excludes all informed search algorithms. There's also randomness involved which excludes all exact solutions. This leaves us with:

* Uninformed search like bfs but with probability
* Machine learning methods
* Bayesian Network
* Reflex agent that accounts for probabilities

Another method that works with all opponent based games is to combine an opponent model with recursion to enhance the performance. This opens up for search tree optimizations such as expectiminimax.

[Are any relevant work being applied to this problem? / what are your references? Explain theories]
refs:
* AIMA
  * A course book, supposed to be usefull
* google crack course
  * Google offers a free course focused on teaching the essentials of ml. They teach what type of ml should be used in different situations aswell as how and why preproccesing is done. 
* keras doc
  * keras documentation offers technical explaination of various algorithms and generalizes the syntax for them. It's gives the mindset that any model reduced to their input dimension, output dimension and model specific parameters. This is intended for structuring large models made of several smaller ad hoc models but the structure helps on smaller projects aswell.  
* scikit doc
  * scikit helps make ml a causal experience. The framework contains all the basic forms of ml aswell as the tools needed to for data processing. The documentation offers many examples on how to use their framework allowing you to stich several examples together rather than getting in depth with the documentation for simple implementations.

# Method
[pick method from introduction and explain the parameters to said method]

As mentioned the chosen method is to make an agent based on machine learning. We'll also give our agent a PEAS descripton 

## Machine learning
Machine learning is a method of generating a model based on past data. By classification or regression, a model is created that represents all the features and their respective target value that aims to create a generalized model. For machine learning, feature selection, data mining and processing are various steps for creating a model. This project utilizes machine learning in the hope of creating a model that can present the data and decide what move the agent should make to gain profit during a round.

### Feature selection
* How did we feature our select
Feature selection was an early stage in which the features or data that are considered to be relevant to each other and which can influence the final decision are examined. From the poker project there are many features such as: Agent and Opponent hand, chips, actions, discarded cards, hand strength and round. However, since drops occurred in the model, the discarded cards and opponent's hand were scrapped as features as they could not generate enough data points for the model.

### Data mining
* How and why?  
Data mining involves extracting and searching for connections between information in large amounts of data. This method extracted the relevant data to be processed. Because it was difficult to extract information from the client side of missed packets and incorrect response, the method was changed to pick data directly from the server. However, the data on the server was not filtered and included information that was not relevant to machine learning. Therefore, only the requested data was extracted which had relevance to all features.

Example 1 below includes two feature vectors where one is an arbitrary feature and example 2 is not considered okay as it lacks important information, which is represented by -1 in the first row.

Example 1:
 * [6255, 250, 2, 250, 250, 250, 250, 'Player_Call', 'Player_Check', 'Player_All-in', None, 'Player_Fold', None, 'Player_Call', 'Player_Check', 'Player_Call', 'Player_Check']

Example 2:

* [-1, 250, 0, 250, 250, 250, 250, 'Player_Fold', None, 'Player_All-in', None, 'Player_Call', 'Player_Check', 'Player_Call', 'Player_Check', 'Player_Call', 'Player_Check']

### Processing
* Normalization
* Quantile
* One-hot-encoding
* 


-PEAS description
"PEAS stands for Performance, Environment, Actuators, and Sensors"
## Performance:
	[Talk about metrics here]

## Enviroment:
Five card poker conatins a set of objects, mechanics and a flow. 

### Objects: 
Serve as achor points for actuators. Could aslo be seen as namespaces
* Chips: A players currency. when it runs out the player loses
* Cards: The building block of hands. Has rank and colour
* Hands: A combination of 5 cards. Given to the player by the game
* The pot: The accumulated bets from all players. 
* Player: The player/agent playing the game. The player owns chips

### Mechanics: 
These are operations/actuators belonging to game objects
* Chips machanics:
	* Match: 
		Means matching the highest current bet
	* Raise:
		Raising means increasing ones bet over the highest current bet which is turn forces all other players to respond. A raise must be equal to or greater than the previous raise, this is to prevent players from stalling the game.
* Cards machanics:
	* Display: cards can be made visible
	* Compare: cards can be compared by both rank and colour
* Hands machanics:
    * Discard: The act of throwing one or more cards which then gets replaced. This action can be seen by all players
	* Display: hands can be made visible
	* Compare: 
	[*insert short/clean explaination here*]

### Flow: 
The operations performed by the game itself. These can be called in any state machine fashion but in this case they are simply called in order.
1. Ante
2. The first betting round is made.
3. If any players remain in the game, then each player can choose to change cards.
4. The second betting round is made.
5. Showdown, where the player hands are compared and the winner(s) will receive the pot (or part of the pot, in case of multiple winners).

## Actuators: 
Mechanics that belong to the player
* Open: Performes the raise actuator from chip without setting the minimum raise.
* Call: Trigger match actuator from chip
* Check: Also triggers chips match actuator
* Raise: Bound to chips raise actuator
* Fold: This actuator is unique for the player. It sets the agent state to folded meaning that the agent will not be affected by the game flow until the start of next round.
* All-in: Raise equal to the players chips.

## Sensors:
	[our feature vector]
	
## xPeke behavior

# Experiment and tournament result
* "What have you observed when playing against a random agent or any agent you have developed?" Server drops, we observed server drops. The f do we write here?
* "Does the result match your expectations?" Had no expectation and was still let down.
* "Observation from the tournament" What tournament

Observations:
During the course of the project, several problems were observed. This includes drop from the server and information did not arrive as expected. This meant that the agents lost the connection to the server and were kicked for incorrect response or lack of response. The messages could come up empty "[]" or with multiple messages in one which caused major learning problems.
After a number of attempts, the idea was abandoned to try to solve the problem and tried to extract the data as well as it could to create a model of the game. Because of the quality of the data from the agents who came up with the project description, it was decided that being in the competition would not give a good idea of ​​how the model is constructed.

Without input data, it is not possible to create a model, so it is no surprise that the model does not work to the extent that would be considered arbitrary. Currently there are 2889 data points to train on, of which 1968 data points are unusable

# Conclusion
[Conclusion is just abstract in reverse. Change my mind]