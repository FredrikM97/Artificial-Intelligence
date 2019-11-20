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
movingTime = 0
minDistance = 0.25
isStuck = False
    
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
	
    closest = World.findEnergyBlocks()[0]
    motorSpeed = dict(speedLeft=0, speedRight=0)
    distanceX = World.getSensorReading('ultraSonicSensorRight')
    distanceY = World.getSensorReading('ultraSonicSensorLeft')
    if distanceX == float("inf"):
        distanceX = 10
    if distanceY == float("inf"):
        distanceY = 10
        
    # In case both is stuck            
    #if distanceX < minDistance and distanceY < minDistance:
    #    World.execute(dict(speedLeft=-2, speedRight=-2), 2000,-1)
    #    World.execute(dict(speedLeft=2, speedRight=-2), 2000,-1)
    #    continue
            
    # Go towards nearest block
    if distanceX > minDistance and distanceY > minDistance:
        motorSpeed = dict(speedLeft=2, speedRight=2)
            
    if isStuck == False:

        if closest[3] < (-1*minDistance) and distanceY > minDistance:
            motorSpeed = dict(speedLeft=-0.5, speedRight=0.5)
        elif closest[3] > minDistance and distanceX > minDistance:
            motorSpeed = dict(speedLeft=0.5, speedRight=-0.5)
        else:
            isStuck = True
    # In case the robot is stuck in area, Then ignore candy and find a way out
    elif isStuck == True:
         # Move left
        if distanceX < minDistance :
            motorSpeed = dict(speedLeft=-3, speedRight=3)
            # Move right
        elif distanceY < minDistance:
                motorSpeed = dict(speedLeft=3, speedRight=-3)
                
    # Stuck handler
    if movingTime <= simulationTime:
            isStuck = not isStuck
            movingTime = simulationTime + 10000

            
    print("right: {} Left {} Closest {} Stuck {} Distance {}".format(distanceX, distanceY, closest[2], isStuck, closest[2]))

    # Try pickup
    if closest[2] < 0.6:
        World.collectNearestBlock()
    
    World.setMotorSpeeds(motorSpeed)
   
