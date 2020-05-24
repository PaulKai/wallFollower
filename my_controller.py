from controller import Robot
import time
TIME_STEP = 64
robot = Robot()
ds = []
dsNames = ['ds_front', 'ds_rightF', 'ds_rightB']
for i in range(3):
    ds.append(robot.getDistanceSensor(dsNames[i]))
    ds[i].enable(TIME_STEP)
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0

def left(distance):
    leftSpeed = -1
    rightSpeed = 1
    a = distance[1] - distance[2]
  
    factor = 1500/1
    wheels[0].setVelocity(leftSpeed-a/factor)   
    wheels[2].setVelocity(leftSpeed-a/factor)
    wheels[1].setVelocity(rightSpeed+a/factor)
    wheels[3].setVelocity(rightSpeed+a/factor)
    print(leftSpeed-a/factor)
    print(rightSpeed+a/factor)
    

def right(distance):
    leftSpeed = 1.0
    rightSpeed = -1
    a = distance[1] - distance[2]
    factor = 1500/1
    wheels[0].setVelocity(leftSpeed+a/factor)   
    wheels[2].setVelocity(leftSpeed+a/factor)
    wheels[1].setVelocity(rightSpeed-a/factor)
    wheels[3].setVelocity(rightSpeed-a/factor)
def forward(distance):
    
    optDist = 900
    Speed = 3
    a = distance[1] - distance[2]
    b = (distance[1] + distance[2])/2 - optDist
    factor = 1500/6
    wheels[0].setVelocity(Speed+(a+b)/factor)
    wheels[2].setVelocity(Speed+(a+b)/factor)
    wheels[1].setVelocity(Speed-(a+b)/factor)
    wheels[3].setVelocity(Speed-(a+b)/factor)
      
             
def fsm(distance):
    global state
    if state == 1:
        right(distance)
        if distance[0] < 1400 and distance[2] < 1400 :
           state = 2
        elif distance[0] > 1000 :
           state = 3     
        return state 


    elif state == 2:
        left(distance)
        if distance[2] > 1400:
           state = 1
        elif distance[0] > 1000:
           state = 3
        return state
    else:
        forward(distance)
        if distance[2] > 1400:
           state = 1
        elif distance[0] < 1400 and distance[2] < 1400:
           state = 2
        return state
                
           
state = 3
dirc = ["right","left","forward"]
while robot.step(TIME_STEP) != -1:
    hs = state
    distance = [ds[0].getValue(),ds[1].getValue(),ds[2].getValue()]
    s = fsm(distance)
    if hs != s:
        print(str(dirc[s-1]))
        #print(distance)
    