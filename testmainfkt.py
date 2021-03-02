from zumi.zumi import Zumi
import time
import Graph_Library as gr
import personalmap as pm
import turning_functions as tf

zumi = Zumi()

IRB = 120
heading = 0

def drivethere(startdirection,startCrossing,EndCrossing,graph):
    path = graph.CalculatePath(startCrossing,EndCrossing)
    currentheading = startdirection
    heading = 0
    speed = 0
    while len(path) != 0:
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
        if currentheading == 'North' and path[0]['direction'] == 'West' or currentheading == 'East' and path[0]['direction'] == 'North' or currentheading == 'South' and path[0]['direction'] == 'East'or currentheading == 'West' and path[0]['direction'] == 'South':
            tf.turnLeft()
        elif currentheading == path[0]['direction']:
            tf.go_straight()
        elif currentheading == 'North' and path[0]['direction'] == 'East' or currentheading == 'East' and path[0]['direction'] == 'South' or currentheading == 'South' and path[0]['direction'] == 'West' or currentheading == 'West' and path[0]['direction'] == 'North':
            tf.turnRight()
        
        path.pop(0)



zumimap = gr.Graph()

zumimap = pm.initPersonalMap(zumimap)
drivethere('North','A','F',zumimap)