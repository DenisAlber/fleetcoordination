# --- Test Code 

from zumi.zumi import Zumi
import time

zumi = Zumi()

zumi.reset_gyro()
speed = 20
heading = 0

for x in range(400): # Take steps
    
    ir_readings = zumi.get_all_IR_data()
    bottom_right_ir = ir_readings[1]
    bottom_left_ir = ir_readings[3]

    if bottom_right_ir > 100 and bottom_left_ir > 100:
        heading = heading       # do nothing
    elif bottom_right_ir < 100 and bottom_left_ir > 100:
        heading += 1.25               # turn left
    elif bottom_left_ir < 100 and bottom_right_ir > 100:
        heading -= 1.25               # turn right
    elif bottom_right_ir < 100 and bottom_left_ir < 100:
            heading -= 6        # drive right in circle    
        
    zumi.go_straight(speed, heading)

zumi.stop()

