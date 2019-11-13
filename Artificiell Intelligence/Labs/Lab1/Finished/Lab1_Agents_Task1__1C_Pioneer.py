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
from random import randrange, uniform
# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

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
    print(closest[3])

    

    # Go towards nearest block
    if closest[3] < 0.1 and closest[3] > - 0.1: # go straight
        #print("Going straight")
        motorSpeed = dict(speedLeft=2, speedRight=2)
    if closest[3] < - 0.1: # Go right
        #print("Going right")
        motorSpeed = dict(speedLeft=1, speedRight=2)
    if closest[3] > 0.1: # Go left
        #print("Going left")
        motorSpeed = dict(speedLeft=2, speedRight=1)
    
    if closest[2] < 0.5:
        #print("Collecting")
        World.collectNearestBlock(
    
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    
