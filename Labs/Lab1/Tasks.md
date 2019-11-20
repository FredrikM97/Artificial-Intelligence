# Tasks
## 1a. Implement an agent that takes random actions.

## 1b. Implement an agent that performs exactly the same sequence of actions all the time, ignoring
sensor input. Try to collect at least 1-2 red blocks.

## 1c. Implement a simple reflex agent that takes sensor input and makes decisions based on the current
sensor readings (no past information should be used).

## 1d. Implement an agent that remembers (some) past sensor readings and actions taken, and utilizes
this information to reach the goal in a more intelligent way. One type of the problem you
probably encounter with the reflex agent is that it gets stuck at some part of the environment
(e.g. in a corner). A very simple way to deal with this is to use a time counter for reaching the
next block’s position. If the robot is taking too much time to reach one of the blocks, it probably
got stuck somewhere, and therefore it should change its strategy to deal with this (see Figure 2).