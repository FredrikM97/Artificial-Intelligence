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
import vrep
import math


def add_new_Sensor(robot):
    new_Sensors = [
        {'name':'Pioneer_p3dx_ultrasonicSensor2','altName': 'left'},
        {'name':'Pioneer_p3dx_ultrasonicSensor4','altName': 'middleLeft'},
        {'name':'Pioneer_p3dx_ultrasonicSensor5','altName': 'middleRight'},
        {'name':'Pioneer_p3dx_ultrasonicSensor7','altName': 'right'}
    ]
    for sensor in new_Sensors:
        
        _,  sensorHandler_ = vrep.simxGetObjectHandle(robot['clientID'], sensor['name'],vrep.simx_opmode_oneshot_wait)
        def factory(sensorHandler_):
            def sensor_method():
                rawSR = vrep.simxReadProximitySensor(robot['clientID'], sensorHandler_, vrep.simx_opmode_oneshot_wait)
            # Calculate Euclidean distance
                if rawSR[1]: # if true, obstacle is within detection range, return distance to obstacle
                    return math.sqrt(rawSR[2][0]*rawSR[2][0] + rawSR[2][1]*rawSR[2][1] + rawSR[2][2]*rawSR[2][2])
                else: # if false, obstacle out of detection range, return inf.
                    return 10
            return sensor_method
        robot[sensor['altName']] = factory(sensorHandler_)
            
# connect to the server
robot = World.init()
add_new_Sensor(robot)
print(sorted(robot.keys()))
movingTime = cooldownTime = 2000
minDistance = 0.4
findTarget = False
speed = 5
rotation = 1.1
prioSearch = 1
state = ''
while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()

    closest = World.findEnergyBlocks()[0]

    SensorRight = (robot['right']())##robot['right']() # Sensor 7
    SensorLeft = (robot['left']()) # Sensor 2
    
    SensorRight1 = (robot['middleRight']()-0.1) # Sensor 5
    SensorLeft1 = (robot['middleLeft']()-0.1) # Sensor 4

    if SensorRight >= SensorRight1:
        SensorRight = SensorRight1
    if SensorLeft >= SensorLeft1:
        SensorLeft = SensorLeft1
    
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

    if closest[2] <= 1.5 and prioSearch < 2 and cooldownTime < simulationTime: 
        findTarget = True
        prioSearch += 1
        movingTime = simulationTime + 4000
    if movingTime < simulationTime and findTarget:
        findTarget = False
        cooldownTime = simulationTime + 4000
        prioSearch = 1

    if closest[2] <= 0.8:
        World.collectNearestBlock()
    
    

    ##############################################
                    # Action:#
    ##############################################
    if not state == 'stuck':
        World.setMotorSpeeds(motorSpeed)