from zumi.zumi import Zumi
import time

zumi = Zumi()

IRB = 120 #IR-Border, point where Black should begin

def turnStraight(heading):
    zumi.calibrate_gyro()
    heading = 0

    for x in range (40):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)

        if bottom_left_ir > IRB or bottom_right_ir > IRB:
            break
        
    zumi.stop()

    for x in range(50):
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]

        if bottom_right_ir > IRB and bottom_left_ir > IRB:
            heading = heading           # do nothing
        elif bottom_left_ir < IRB and bottom_right_ir < IRB:
            break
        elif bottom_right_ir < IRB:
            heading += 1              # turn left
            
        elif bottom_left_ir < IRB:
            heading -= 1               # turn right
            
        
        zumi.go_straight(20, heading)
        print(x)
    zumi.stop()

            
    


def turnRight():
    zumi.calibrate_gyro()
    heading = 0
    for x in range (300):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)
        
        if heading > -71:
            heading -= 4
            print("In Winkel")
        
        print(heading)


        if heading < -51 and (bottom_left_ir > IRB or bottom_right_ir > IRB):
            zumi.stop()
            break

    for x in range (40):
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]

        if bottom_right_ir > IRB and bottom_left_ir > IRB:
            heading = heading           # do nothing
            
        elif bottom_left_ir < IRB and bottom_right_ir < IRB:
            break
        elif bottom_right_ir < IRB:
            heading += 1              # turn left
            
        elif bottom_left_ir < IRB:
            heading -= 1               # turn right
        
        zumi.go_straight(20, heading)
    
    zumi.stop()



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

for x in range(2000): # Take steps
    
    ir_readings = zumi.get_all_IR_data()
    bottom_right_ir = ir_readings[1]
    bottom_left_ir = ir_readings[3]

    if bottom_right_ir > IRB and bottom_left_ir > IRB:
        heading = heading           # do nothing
        
    elif bottom_left_ir < IRB and bottom_right_ir < IRB:
        break
    elif bottom_right_ir < IRB:
        heading += 1              # turn left
        
    elif bottom_left_ir < IRB:
        heading -= 1               # turn right
        
    
    zumi.go_straight(speed, heading)

zumi.stop()
turnRight()




    