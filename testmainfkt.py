from zumi.zumi import Zumi
import time
import Graph_Library as gr
import personalmap as pm
import turning_functions as tf
from zumi.util.screen import Screen

zumi = Zumi()
screen=Screen()
IRB = 120


def drivethere(startdirection,startCrossing,EndCrossing,graph):
    path = graph.CalculatePath(startCrossing,EndCrossing)
    currentheading = startdirection
    heading = 0
    speed = 30
    lastCrossing = None
    nextCrossing = None
    
    while len(path) != 0:
        zumi.reset_gyro()
        heading = 0
        for x in range(2000): # Take steps
        
            ir_readings = zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]

            if bottom_right_ir > IRB and bottom_left_ir > IRB:
                heading = heading           # do nothing
                
            elif bottom_left_ir < IRB and bottom_right_ir < IRB and x > 10:
                break
            elif bottom_left_ir < IRB and bottom_right_ir < IRB:
                zumi.stop()
                if tf.fixZumiPosition(lastCrossing,nextCrossing):
                    screen.clear_display()
                    screen.draw_text("Thank you")
                    time.sleep(1.0)
                    screen.clear_display()
                    zumi.reset_gyro()
                    heading = 0
                    
                else:
                    print("This Boy is gone")
                    return False
                
            elif bottom_right_ir < IRB:
                heading += 0.5              # turn left
                
            elif bottom_left_ir < IRB:
                heading -= 0.5               # turn right
                
            
            zumi.go_straight(speed, heading)
        zumi.stop()
        
        print("off")
        print("bheading: " + str(heading))
        print("bGyro: " + str(zumi.read_z_angle()))
        direc = str(input())
        
        if currentheading == 'North' and path[0]['direction'] == 'West' or currentheading == 'East' and path[0]['direction'] == 'North' or currentheading == 'South' and path[0]['direction'] == 'East'or currentheading == 'West' and path[0]['direction'] == 'South':
            tf.turnLeft()
            print("left")
        elif currentheading == path[0]['direction']:
            tf.turnStraight()
            print("straight")
        elif currentheading == 'North' and path[0]['direction'] == 'East' or currentheading == 'East' and path[0]['direction'] == 'South' or currentheading == 'South' and path[0]['direction'] == 'West' or currentheading == 'West' and path[0]['direction'] == 'North':
            tf.turnRight()
        elif currentheading == 'North' and path[0]['direction'] == 'South' or currentheading == 'East' and path[0]['direction'] == 'West' or currentheading == 'South' and path[0]['direction'] == 'North' or currentheading == 'West' and path[0]['direction'] == 'East':
            tf.turnAround()
        print("aheading: " + str(heading))
        print("aGyro: " + str(zumi.read_z_angle()))
        currentheading = path[0]['direction']
        lastCrossing = path[0]['currentCrossing']
        nextCrossing = path[0]['nextCrossing']
        path.pop(0)



zumimap = gr.Graph()

zumimap = pm.initPersonalMap(zumimap)
drivethere('South','G','A',zumimap)