# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import Lab1_Agents_Task1_World as World
from random import randrange, uniform, randrange
import math

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))
movingTime = 10000
minDistance = 0.35
isStuck = False
speed = 2
rotation = 2
prioSearch = 1
currentTarget = 0
while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    if simulationTime%1000==0:
        # print some useful info, but not too often
        print ('Time:',simulationTime,\
               'ultraSonicSensorLeft:',World.getSensorReading("ultraSonicSensorLeft"),\
               "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
	
    closest = World.findEnergyBlocks()[currentTarget]
    motorSpeed = dict(speedLeft=0, speedRight=0)
    distanceX = World.getSensorReading('ultraSonicSensorRight')
    distanceY = World.getSensorReading('ultraSonicSensorLeft')
    if distanceX == float("inf"):
        distanceX = 10
    if distanceY == float("inf"):
        distanceY = 10
        2
    # In case both is stuck            
    #if distanceX < minDistance and distanceY < minDistance:
    #    World.execute(dict(speedLeft=-2, speedRight=-2), 2000,-1)
    #    World.execute(dict(speedLeft=2, speedRight=-2), 2000,-1)
    #    continue
            
    # Go towards nearest block
    if distanceX > minDistance or distanceY > minDistance:
        motorSpeed = dict(speedLeft=speed, speedRight=speed)
    else:
        World.execute(dict(speedLeft=speed, speedRight=-speed), 1000,-1)
    if isStuck == False:
        if closest[3] < (-1*minDistance) and distanceY > minDistance:
            motorSpeed = dict(speedLeft=-rotation, speedRight=rotation)
        elif closest[3] > minDistance and distanceX > minDistance:
            motorSpeed = dict(speedLeft=rotation, speedRight=-rotation)

    # In case the robot is stuck in area, Then ignore candy and find a way out
    elif isStuck == True:
        # Conditional move
        if prioSearch > 4:
            rotation = uniform(2,4)
        if prioSearch > 20**(currentTarget+1) and len(World.findEnergyBlocks()) > currentTarget:
            currentTarget = currentTarget +1
            
        if distanceX < minDistance and distanceY > distanceX:
            motorSpeed = dict(speedLeft=-rotation, speedRight=rotation)
        elif distanceY < minDistance and distanceX > distanceY:
            motorSpeed = dict(speedLeft=rotation, speedRight=-rotation)
        elif distanceX < minDistance:
            motorSpeed = dict(speedLeft=-(rotation+1), speedRight=(rotation+1))
        elif distanceY < minDistance:
            motorSpeed = dict(speedLeft=(rotation+1), speedRight=-(rotation+1))

    # Stuck handler
    if movingTime <= simulationTime:
            isStuck = not isStuck
            movingTime = simulationTime + 2000*prioSearch
            prioSearch = prioSearch + 1

            
    #print("right: {} Left {} Closest {} Stuck {} Distance {}".format(distanceX, distanceY, closest[2], isStuck, closest[2]))
    print("Closest {} Stuck {} Distance {} Prio {}".format(closest[2], isStuck, closest[2], prioSearch))

    # Try pickup
    if closest[2] < 0.6:
        World.collectNearestBlock()
        movingTime = simulationTime + 2000
        prioSearch = 1
        currentTarget = 0
    
    World.setMotorSpeeds(motorSpeed)
   
