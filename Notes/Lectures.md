<!-- https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols -->
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
* So $\alpha$ is my player, $\beta$ is the opponent. Root will be the $\alpha$, then it takes turn between $\beta$ and $\alpha$

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

# Lecture 5 (12/11-2019)
## Logical agent
* Search algorithms $\rightarrow$ meta programming
* Something more logical needded were we can specify rules

PEAS description (The wumpus world example):
* Performance measure: +1000 gold, -1000 falling into pit/eaten by monster, -1 per action, -10 by using arrow
* Environment: 4x4 grid
* Actuators: Move, turn (right,left), grab shoot
* Sensors
  
Exploring the world (Example)
* At start position: $x_{1,1} = (0,0,0,0,0)$, size dependant on PEAS description about the world
* Checking $x_{1,1} = (1,0,0,1,0)$, breezee and smell found
* And so on..

## Logic
* Formal language for representing information so conclusions can be drawn

Logic has:
* Syntax: Symbols in represention language and how they are combined into sentences
* Semantics: Facts about the world and what they refers to
* Inference procedure: New sencenece from previous sentences

Entailment $A |= B$:
* Sencence A entails the sencence B
  * If A is true then be must be true

Interference engine
* Algorithm that produces the entailed conclusions automatically
  * For any user defined knowledge base

Propositional (boolean) logic
* Atomic sentence
* Complex sentence
  
Semantics: Rules for sencence is true or false


Automate Inference:

* Model enumeration
* Inference rules
Inference rules:

* Atecedent / Consequent = "Before"/"After".
* If KB contains the antecedent it we can add the consequent because it is guaranteed KB will entail it

Common used inference rules:

* Modus Ponens And Elimination
* Modus Tolens or Introduction
* Unit Resolution and Introduction

## Horn clauses and forward-backward chaining
Forward chaining:
* Use current facts in KB to trigger all possible inferences

Backward chaining:
* Work backward from the query proposition Q
* If a rule has Q as conclusion, see if antecedents can be found to be true

## Summary of lecture
Repersation language has syntax and semantics
Proporsitional logic
* Proposition symbols
* Logical connectives 
Interference:
* Model checking
* Interference rules (e.g resolution)
* Horn clauses

# Lecture 6 (18/11-2019)

Why first order logic? (FOL)
* Propositional logic:: Create an generalisation of the object. Instead of specify each object from the beginning

Syntax:
* Lgical symbols: Logical connectivives, quantifiers, equality symbols and truth constants
* Non-logical symbols: Constants(objects), predicates, Functions

Term
1. Object constant is a term
2. Complete functions containt is a term

Well-formed formula (wff)
* wff is something that could be true or false
  1. Complete predicate sumbols is a wff
  2. Equality between to terms
  3. Negation of a wff is a wff
  4. Two wffs connected by a connective is a wff

Variables: unspecified onbjects in the domain
Sentence: Well formed formula without any free variables

* Atomic sentence: Complete predicate symbol (relation), comes from model/interpretation
* Complex sentence: FOrmed by sentences and connectives, determined by truth tables
  

Contexts:
* $\forall:$ For all
* $\exists:$ For someone exists
* $\land:$ And
* $\lor:$ Or
  
Example:
* $\forall_x$ King(x) $\implies$ Person(x) - All kings are persons)
* $\exists_x$ At(x,Stanford) $\lor$ Smart(x) - Someone at stanfod is smart

Order matter!! Example:
* $\forall_x$ $\exists_y$ Loves(x,y) - Everybody loves somebody
* $\exists_y$ $\forall_x$ Loves(x,y) - Somebody is loved by everyone
  
With deMorgan:
* $\exists_x \neg P(x) \equiv \neg\exists_x P(x)$
* ....


Additional:
A mother is a female parent
* $\forall_{x,c}$ Female(mother(x) $\land$ Parent(Mother(c),c))

## Reduce to propositional logic
* Model checking
* Resolution

Universal instantiation (UI)
Existential Instantiation (EI)

UI + EI => propositional sentence

# Lecture 7 (19/11-2019)
Problems:
* Partial observability
* Noise sensors
* Uncertainty in action of outcomes
* Immense complexity in modelling and predicting state of the environment
  
Why FOL fail:
* Laziness: 
* Ignorance
* Practical reasons

Solution: Decision theory:
* Decision theory = Probability theory + utility theory
  
Probability:
1. Probability to a proposition based on the percepts (info the agent have)
2. Proposition is either true or false
3. Evidence is information that the agent receives
4. Propr/unconditional probability
5. Posterior/conditional probability

Utility:
1. Plan doesnt need to guarantee to acheive the goal
2. To make choices
3. ...


Interpretation of probability:
* CLassic interpretation
* Frequence interpretation
* Bayesian Interpretation


Full joint distribution

# Lecture 8 (25/11-2019)
Naive Bayes
Bayesian networks

# Lecture 9 (2/12-2019)
Types of learning:
* Deductive (learning from existing data)
* Inductive (learning from experience)
  
Data mining:
* Historical data to improve decisions

    * Software engineering
    * Self-customising program

Inductive learning:
* Supervised (Correct itself towards the answer)
* Reinforced (Given feedback concerning the decision it makes)
* Unsupervised (No feedback, need to search order and structure in environment)

## Supervised learning

Classification:
* Learning categories
* mark new items as interesting/uninteresting
* Diagnose desease
* "Place in buckets" -Discrete values
  
Regression: 
* Learning function values (generative model)
* Numerical output
* Future stoock market value
* Continuous values

Generalized function:
* Works for multiple sets of data (ex: temperature in sweden and africa)
Ockhams razor: Take the simplest hypothesis

## Training algorithms
Find-S algorithm: Find a generalised model
List-Then-Eliminate Algorithm

Version space
UNBIASED Learning: 
* Use disjunctions, conjunctions, negations over attribute constraints

Inductive Bias

Decision tree:
* Simplest
* Advanced
* True tree vs inductive tree

PAC: Probability approximately correct:
- Lower sample size $\rightarrow$ Higher chance for error
Generalization error:
* Unseen scenarios in training set

# Lecture 10 (9/12-2019)
McCulloch-Pitts model

Perception learning:
* Guaranteed to find solution in finite time, if solution exists
* Cannt be generalized to more complex networks
* Better to use gradient descent - Based on the formulation an error and differentiable functions

When to stop learning using gradient descent:
* When change becomes smaller than certain number
* Validation data - "early stop"

SVM (support vector machine)




