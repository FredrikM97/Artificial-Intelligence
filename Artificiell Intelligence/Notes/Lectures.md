
# Lecture 1 (4/11-2019)

Introduction
How computers represent knowledge:
* Symbolic (logic) and nosymbolic (neural networks)

## Lectures
1) Introduction 1&2
2) Informed search 3
3) Adversarial Search 5
4) Porpositional logic 7
5) First-order logic 8&9
6) Uncertainty/Probability 13&16
7) .. More in lecture 1 powerpoint

## Fundamental issues
* Sensing, Representation, Search, Interference, Learning, Planning

## Agent
Reflex agent:
* An agent perceives its environment though sensors and act upon that though effectors

Rational agent:
* "The right thing", For each possible percept sequence - select the action that is expected to maximise its performance measure.
* Rationality $\neq$ Optimality
* No future observations
* Optimality = Rationality + Omniscience

## Performance control
* State definced performance measure
* Action defined performance measure

## Task Description
Describe what the agent can do and how the environment is (from powerpoint example).
* Performance measure: Maximize number of clean cells & minimize number of dirty cells
* Environment: Discrete cells, either dirt or clean, Static, deterministic and sequential
* Actuators: Engine and & wheels
* Sensors: Dirty, filthy, clean room

## Environment Types
* Single vs multi-agent
* Accessible vs inaccessible
* Deterministic vs nondeterministic (Will the result always be the same?)
* Static vs dynamic environment
* Discrete vs continuous

## Classes of Agents
* Random
* Fixed (or sequential)
* Reflex agent 
    1) No internal memory
    2) Can be simple (table lookup) or very complex)
* Model-based agent: Knowledge of world though a model
* Goal-based agent
* Utility-based 
* Learning agent 

# Lecture 2 (5/11-2019)

## Uninformed search algorithm
* Initial state  $\theta(0)$
* List of possible actions \alpha -> for agents
* Goal test
* Path cost

One solution $\theta(0)$ -> $\theta(1)$ -> .. -> $\theta(N)$

Different algorithms for uninformed search:
1) Breadth-first
2) Depth-first
3) Iteratiev deepening

## Evaluation of algorithm
* Completeness
* Optimality 
* Time complexity (Number of nodes expanded during search)
* Space complexity (maz number of nodes in memory)

## A* search algorithm
* Good for calculating distance between points (example an map)
* Higher value (sum) lower priority in list
* Distance 1 + Distance 2 (straight line) from point to finish
  * Distance 1 handle how far between nodes
  * Distance 2 tells if we get further or closer to goal


# Lecture 3 (Laboration introduction)
Create four different agents
* Random agent (random event)
* Fixed agent (Fixed frequence of actions)
* Reflex agent (Check if conditions are met)
* Agent with memory (Remember past decisions)

Mobile robot
- 

# Lecture 4 (11/11-2019)
## Adversarial search:
* Planing ahead against the opponent
* "Two or more players with conflicting goals trying to explote same space for the solution, aka adversarial searches or even known as Games

Example states in Tick tack toe:
* Initial state:
    3x3 empty table
* Successor function:
    Take turn making X or O in table
* Goal state:
    When all the tables are filled
* Utility function:
Add +1 for three in row, -1 if the opponent have 3 in a 

## Minimax principle
Assume the opponent plays to win and always make the best possible move (Test by doing a graph of all possible combination were AI try to win)

Terminology: Max  = You, Min = the opponent

Definition: Minimax value for node n:
    Utility(n)
    Max(Minimax values of successor)
    Min(Minimax values of successor

Higher utility favours your MAX, choose the highest utility, Lower utility favours the opponent
* Depth-first search: TIme complexity O($b^d$), Space complexity: O($bd$), Takes longer time but uses less space
* The time complexity impossible in real games (with time constrains) except in very simple games. 

Improvements:
* Remove redundant search paths: Symmetries
* Remove unintresting search paths (Paths opponent never will choose): Alpha-beta pruning
* Cut the search short before goal: Evaluation functions
* Book moves

Example of redundant paths:
    Mirror symmetries and rotational symmetry can be removed
    By putting an X in a corner it will represent all 4 possibilities that include a single corner. Same is included for middle position.
    Therefor: 3 states instead of 9 and for second stage it will be 12 states instead of 8*9=72.

## alpha-beta pruning rule
Example uninteresting paths 
* If player has better choice m at n's parent node or any node further up the node n will never be reached (Under the condition that the player isnt stupid)
* According to alpha-beta example: If $\alpha >= \beta$ then dont go further down into $\beta$ path.
* In graph, $\alpha$ want to be as high (positive) as possible and $\beta$ want to be as low as possible (negative), Depth limit reached when it doesnt choose that path.
* So $\alpha$ is my player, $\=beta$ is the opponent. Root will be the $\alpha$, then it takes turn between $\beta$ and $\alpha$

## Evaluation Function (Missing data)
$f(n) = W_i$....2..

## Reinforcement learning
A method to learn an evaluation function, for chess
* Assign a bit of the goal node's ultility value to the next last square 
* Example: Robot learn to naigate in a maze, number all path points, Highest value that is closest should be the path to take?
* Takes a long time to do though

## Games with chance
* Extend the minimax tree with chance layers

## Local search
From initial state (NxN chessboard), try to move to other configurations such that the number on conflicts is reduced

Hill-climbing:
* Current node $n_i$
* Grab neighboor node $n_{i+1}$ and move there if it improves things, if $\delta f = f(m_i)-f(n_{i+1} > 0)$

Local beam search:
* Start with k random states
* Expand all k states and test their children states
* Keep the k best children state
* Repeat until goal state found
