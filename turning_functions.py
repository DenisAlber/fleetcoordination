from zumi.zumi import Zumi
import time

zumi = Zumi()

IRB = 120 #IR-Border, point where Black should begin

def turnStraight():
    zumi.reset_gyro()
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
        
    zumi.stop()
    print("heading: " + str(heading))
    print("Gyro: " + str(zumi.read_z_angle()))
    return heading

            
def turnAround():
    zumi.reset_gyro()
   
    zumi.left_u_turn(speed=20, step=6, delay=0.02)
    zumi.reset_gyro()
    heading = 0
    lf = False
    rf = False
    counter = 0
    for x in range (34):
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
      
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
       
        zumi.go_straight(10, heading)
            
    zumi.stop()
    return heading


def turnRight():
    zumi.reset_gyro()
    heading = 0
    
    for x in range (1000):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)
        
        if heading > -73:
            heading -= 4
          


        if heading < -75 and (bottom_left_ir > IRB or bottom_right_ir > IRB):
            zumi.stop()
            
            break
    
    counter = 0
    lf = False
    rf = False
    for x in range (35):  #bisheriges optimum 34 steps
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
      
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
       
        zumi.go_straight(10, heading)
            
    zumi.stop()
    print("heading: " + str(heading))
    print("Gyro: " + str(zumi.read_z_angle()))
    return heading



def turnLeft():

    zumi.reset_gyro()
    heading = 0
    
    
    for x in range (40):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)

        if bottom_left_ir > IRB or bottom_right_ir > IRB:
            break

    for x in range(16):
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
    
    for x in range (100):

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
        zumi.go_straight(20, heading)
        
        if heading < 73:
            heading += 4
            


        if heading > 73 and (bottom_left_ir > IRB or bottom_right_ir > IRB):
            zumi.stop()
         
            break
    counter = 0
    lf = False
    rf = False
    for x in range (35):
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]
        
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
        
        zumi.go_straight(10, heading)
    zumi.stop()
    print("heading: " + str(heading))
    print("Gyro: " + str(zumi.read_z_angle()))
    return heading
        
    









    