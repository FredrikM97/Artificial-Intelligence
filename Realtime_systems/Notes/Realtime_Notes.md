# Seminar study Notes
## Introduction 
* Purpose to schedule two kinds of tasks:
* Periodic that is indepentent with known properties that is known in advance
* Sporadic that is more unpredictable with timing and predecence constraints.
* So the tasks at hand is how to decide if we should accept or block an incomming sporadic tasks.

* The test that have been done accoding to the paper is done on a single processor machine

-
## New results
* The new approach is to combine dependent and indepentent tasks and convert dependent tasks into independent.
* This will give advantages such as no discrimination between Dependent and independent tasks
* The modifications will ensure that predecence contrains is still obeyed after ED
* Not necessary to construct the schedule to prove that all deadlines can be met.

### Algorithm
* The idea is to depend on the deadline and the deadline of its successor
* And the starting time of task depends on the release time and completion time of predecessors

These are the variables that is used.

* First part is to handle the modified deadline, and its successor as it can be seen on the slide

* Second is to handle the modified release time, and its predecessor

After the following operations we have obtained an equivalent scheduling problem. 

Thereafter we construct a valid schedule by applying ED to the independent task and supplied with timing parameters.
This mean that we now have a priority list with the following critera. 
* The report showes a proof of the method and come to a conclusion were the scheduability of S implies scheduability of the successor
* And that the relations are always obeyed, both timing and precedence contrainsts is met according to ED
