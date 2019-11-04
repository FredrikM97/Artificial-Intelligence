
# 1. Lecture 1 (4/11-2019)

Introduction
How computers represent knowledge:
* Symbolic (logic) and nosymbolic (neural networks)

## 1.1. Lectures
1) Introduction 1&2
2) Informed search 3
3) Adversarial Search 5
4) Porpositional logic 7
5) First-order logic 8&9
6) Uncertainty/Probability 13&16
7) .. More in lecture 1 powerpoint

## 1.2. Fundamental issues
* Sensing, Representation, Search, Interference, Learning, Planning

## 1.3. Agent
Reflex agent:
* An agent perceives its environment though sensors and act upon that though effectors

Rational agent:
* "The right thing", For each possible percept sequence - select the action that is expected to maximise its performance measure.
* Rationality $\neq$ Optimality
* No future observations
* Optimality = Rationality + Omniscience

## 1.4. Performance control
* State definced performance measure
* Action defined performance measure

## 1.5. Task Description
Describe what the agent can do and how the environment is (from powerpoint example).
* Performance measure: Maximize number of clean cells & minimize number of dirty cells
* Environment: Discrete cells, either dirt or clean, Static, deterministic and sequential
* Actuators: Engine and & wheels
* Sensors: Dirty, filthy, clean room

## 1.6. Environment Types
* Single vs multi-agent
* Accessible vs inaccessible
* Deterministic vs nondeterministic (Will the result always be the same?)
* Static vs dynamic environment
* Discrete vs continuous

## 1.7. Classes of Agents
* Random
* Fixed (or sequential)
* Reflex agent 
    1) No internal memory
    2) Can be simple (table lookup) or very complex)
* Model-based agent: Knowledge of world though a model
* Goal-based agent
* Utility-based 
* Learning agent 
## 