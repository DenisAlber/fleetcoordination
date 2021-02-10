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
    for x in range (1000):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)
        
        if heading > -73:
            heading -= 4
            print("In Winkel")
        
        print(heading)


        if heading < -75 and (bottom_left_ir > IRB or bottom_right_ir > IRB):
            zumi.stop()
            print("line follower")
            break
    print("leave")
    counter = 0
    lf = False
    rf = False
    for x in range (35):
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        print("step " + str(x))
        print(bottom_left_ir)
        print(bottom_right_ir)
        if bottom_right_ir > IRB and bottom_left_ir > IRB:
            heading = heading           # do nothing
            lf = False
            rf = False
            
        
        elif bottom_right_ir < IRB and lf == False:
            heading += (3.5 - counter *0.1)              # turn left
            rf = True
            counter = counter +1
            
        elif bottom_left_ir < IRB and rf == False:
            heading -= (3.5 - counter * 0.1)               # turn right
            lf = True 
            counter = counter +1
        print("counter" + str(counter))
        zumi.go_straight(10, heading)
        """
        if counter == 30:
            print("leave be angle")
            break
        """        
    zumi.stop()
    return heading



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
heading = turnRight()

for x in range(20): # Take steps
    
    ir_readings = zumi.get_all_IR_data()
    bottom_right_ir = ir_readings[1]
    bottom_left_ir = ir_readings[3]

    if bottom_right_ir > IRB and bottom_left_ir > IRB:
        heading = heading           # do nothing
        
    elif bottom_left_ir < IRB and bottom_right_ir < IRB:
        print("raus bruder")
        break
    elif bottom_right_ir < IRB:
        heading += 1              # turn left
        
    elif bottom_left_ir < IRB:
        heading -= 1               # turn right
        
    
    zumi.go_straight(speed, heading)
zumi.stop()




    