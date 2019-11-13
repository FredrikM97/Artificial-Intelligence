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
movingTime = 2000
movingTime2 = 2000
minDistance = 0.4
findTarget = False
speed = 5
rotation = 1.1
prioSearch = 1
currentTarget = 0
executeTime = 0
state = ''
while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()

    closest = World.findEnergyBlocks()[currentTarget]

    SensorRight = World.getSensorReading('ultraSonicSensorMoreRight') # Sensor 7
    SensorLeft = World.getSensorReading('ultraSonicSensorMoreLeft')# Sensor 2

    SensorRight1 = (World.getSensorReading('ultraSonicSensorRight')-0.1) # Sensor 5
    SensorLeft1 = (World.getSensorReading('ultraSonicSensorLeft')-0.1) # Sensor 4

    if SensorRight >= SensorRight1:
        SensorRight = SensorRight1
    if SensorLeft >= SensorLeft1:
        SensorLeft = SensorLeft1
    
    if SensorRight == float("inf"):
        SensorRight = 10
    if SensorLeft == float("inf"):
        SensorLeft = 10
    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
	
    

    if SensorRight < minDistance and SensorRight < SensorLeft:
        state = 'left'
    elif SensorLeft < minDistance and SensorLeft < SensorRight:
        state = 'right'
    else:
        state = 'forward'

    
    if round(SensorRight,2) == round(SensorLeft,2) and  round(SensorLeft,2) <= 0.38:
        state='stuck'

    elif findTarget and movingTime >= simulationTime:
        if closest[3] < (-1*0.3) or SensorRight < minDistance:
            state = 'left'
        elif closest[3] > 0.3 or SensorLeft < minDistance:
            state = 'right'
        else:
            state = 'forward'
    

    ######## State machine ########
    if state == 'left':
        motorSpeed = dict(speedLeft=-rotation, speedRight=rotation)
    elif state == 'right':
        motorSpeed = dict(speedLeft=rotation, speedRight=-rotation)
    elif state == 'stuck':
        World.execute(dict(speedLeft=rotation, speedRight=-rotation),2000,-1)
    elif state == 'forward': # Forward
        motorSpeed = dict(speedLeft=(speed+0.3), speedRight=speed)

    print("State {0}\tSearch {1} Distance {2:.4f} Prio {3} \n Right: {4:.2f} Left: {5:.2f}".format(state, findTarget, closest[2], prioSearch , round(SensorRight,2), round(SensorLeft,2)))

    # Try pickup

    if closest[2] <= 1.5 and prioSearch < 2 and movingTime2 < simulationTime: #and prioSearch < 4 and movingTime2 < simulationTime:
        findTarget = True
        prioSearch += 1
        movingTime = simulationTime + 4000
    if movingTime < simulationTime and findTarget:
        findTarget = False
        movingTime2 = simulationTime + 4000
        prioSearch = 1

    if closest[2] <= 0.8:
        World.collectNearestBlock()
    
    

    ##############################################
                    # Action:#
    ##############################################
    if not state == 'stuck':
        World.setMotorSpeeds(motorSpeed)