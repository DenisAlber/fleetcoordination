from zumi.zumi import Zumi
import time
import turning_functions as tf


zumi = Zumi()

IRB = 120

while True:

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
    print("Type direction: ")
    direc = str(input())

    if direc == "g":
        heading = tf.turnStraight()
    elif direc == "r":
        heading = tf.turnRight()
    elif direc == "l":
        heading = tf.turnLeft()
    else:
        break

    print("Fertig")
    direc = str(input())
