from zumi.zumi import Zumi
import time

zumi = Zumi()

def turnStraight():
    zumi.calibrate_gyro()
    heading = 0
    for x in range (300):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)

        if bottom_left_ir > 100 or bottom_right_ir > 100:
            zumi.stop()
            print("yeah")
            break

def turnRight():
    zumi.calibrate_gyro()
    heading = 0
    for x in range (300):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)
        
        heading -= 3.5
        print(heading)


        if bottom_left_ir > 100 or bottom_right_ir > 100:
            zumi.stop()
            print("yeah")
            break


def turnLeft():

    zumi.calibrate_gyro()
    heading = 0
    for x in range (300):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)
        
     
        heading += 2
        
       


        if bottom_left_ir > 100 or bottom_right_ir > 100:
            zumi.stop()
            print("yeah")
            break





zumi.reset_gyro()
speed = 30
heading = 0
while True:
    for x in range(2000): # Take steps
        
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]

        if bottom_right_ir > 100 and bottom_left_ir > 100:
            heading = heading           # do nothing
            offcounter = 0
        elif bottom_left_ir < 100 and bottom_right_ir < 100:
            break
        elif bottom_right_ir < 100:
            heading += 0.5              # turn left
            
        elif bottom_left_ir < 100:
            heading -= 0.5               # turn right
            
        
        zumi.go_straight(speed, heading)

    zumi.stop()
    turnLeft()
    break


        