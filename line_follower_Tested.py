from zumi.zumi import Zumi
import time

zumi = Zumi()

zumi.reset_gyro()
speed = 30
heading = 0

for x in range(40): # Take steps
    
    ir_readings = zumi.get_all_IR_data()
    bottom_right_ir = ir_readings[1]
    bottom_left_ir = ir_readings[3]

    if bottom_right_ir > 100 and bottom_left_ir > 100:
        heading = heading           # do nothing
    elif bottom_right_ir < 100:
        heading += 5               # turn left
    elif bottom_left_ir < 100:
        heading -= 5               # turn right
    zumi.go_straight(speed, heading)

zumi.stop()