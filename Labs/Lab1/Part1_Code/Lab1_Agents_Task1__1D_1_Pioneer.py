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
checkStuck = 0
oldPos = 0
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
	
    # TODO
    # Find closest, args(blockHandle, blockName, distance, direction)
    # Get direction, if direction is less than keep going forward
    # If object in the way Try going around (random ish)

    closest = World.findEnergyBlocks()[0]
    print("Position: {} and Old Position {}, Stuck: {}".format(closest[2], oldPos, checkStuck))
        
    if  checkStuck == 15: # World.getSensorReading('ultraSonicSensorLeft') < 0.2 or World.getSensorReading('ultraSonicSensorLeft') < 0.2 or
        checkStuck = 0
        rotation = (-1)**randrange(2)
        print(rotation)
        World.execute(dict(speedLeft=(-1*rotation*2), speedRight=(rotation*2)),1350,-1)
        World.execute(dict(speedLeft=2, speedRight=2),4000,-1)
        
    else:
        # Go towards nearest block
        if closest[3] < 0.1 and closest[3] > - 0.1: # go straight
            #print("Going straight")
            motorSpeed = dict(speedLeft=2, speedRight=2)
            
        if closest[3] < - 0.1:# or World.getSensorReading('ultraSonicSensorLeft') < 0.1: # Go right
            #print("Going right")
            motorSpeed = dict(speedLeft=1, speedRight=2)
        if closest[3] > 0.1: #or World.getSensorReading('ultraSonicSensorRight') < 0.1: # Go left
            #print("Going left")
            motorSpeed = dict(speedLeft=2, speedRight=1)
        # Check if it is stuck while trying to move forward
        if oldPos - 0.001 <= closest[2] and oldPos + 0.001 >= closest[2]:
            checkStuck  = checkStuck + 1
        
        World.setMotorSpeeds(motorSpeed)

    if closest[2] < 0.5:
        World.collectNearestBlock()
        checkStuck = 0
    oldPos = closest[2]
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    
    
    
