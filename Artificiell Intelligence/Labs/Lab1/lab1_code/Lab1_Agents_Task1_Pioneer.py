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
minDistance = 0.4
isStuck = False
speed = 2
rotation = 0.3
prioSearch = 1
currentTarget = 0
executeTime = 0
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

    distanceX1 = (World.getSensorReading('ultraSonicSensorMoreRight')-0.2)
    distanceY1 = (World.getSensorReading('ultraSonicSensorMoreLeft')-0.2)
    if distanceX >= distanceX1:
        distanceX = distanceX1
    if distanceY >= distanceY1:
        distanceY = distanceY1
    
    if distanceX == float("inf"):
        distanceX = 10
    if distanceY == float("inf"):
        distanceY = 10

    # Go towards nearest block
    motorSpeed = dict(speedLeft=(speed+0.05), speedRight=speed)

    if isStuck == False:
        if closest[3] < (-1*0.3) or distanceY < minDistance:
            motorSpeed = dict(speedLeft=-rotation, speedRight=rotation)
        elif closest[3] > 0.3 or distanceX < minDistance:
            motorSpeed = dict(speedLeft=rotation, speedRight=-rotation)

    # In case the robot is stuck in area, Then ignore candy and find a way out
    elif isStuck == True:
        # Conditional move
        if prioSearch > 4 or simulationTime % 6000 == 0:
            rotation = uniform(1,3)
        if prioSearch > 20**(currentTarget+1) and len(World.findEnergyBlocks()) > currentTarget:
            currentTarget = currentTarget +1

        if distanceX < minDistance and distanceY > distanceX:
            motorSpeed = dict(speedLeft=-rotation, speedRight=rotation)
        elif distanceY < minDistance and distanceX > distanceY:
            motorSpeed = dict(speedLeft=rotation, speedRight=-rotation)
        elif distanceX < minDistance:
            motorSpeed = dict(speedLeft=-(rotation), speedRight=(rotation))
        elif distanceY < minDistance:
            motorSpeed = dict(speedLeft=(rotation), speedRight=-(rotation))

    # Stuck handler
    if movingTime <= simulationTime:
            isStuck = not isStuck
            movingTime = simulationTime + 2000*prioSearch
            prioSearch = prioSearch + 1

            
    #print("right: {} Left {} Closest {} Stuck {} Distance {}".format(distanceX, distanceY, closest[2], isStuck, closest[2]))
    print("Closest {} Stuck {} Distance {} Prio {}".format(closest[2], isStuck, closest[2], prioSearch))

    # Try pickup
    if closest[2] < 0.9:
        World.collectNearestBlock()
        movingTime = simulationTime + 2000
        prioSearch = 1
        currentTarget = 0
    

    # Do the action
    World.setMotorSpeeds(motorSpeed)