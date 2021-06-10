from long_polling import WaitThread
import requests
import json
import threading
import time

import Graph_Library as gr
import personalmap as pm
import turning_functions as tf

from zumi.zumi import Zumi
from zumi.util.screen import Screen
from zumi.util.camera import Camera
from zumi.util.vision import Vision

zumi = Zumi()
camera = Camera()
vision = Vision()
screen=Screen()

IRB = 120
speed = 30

zumiMap = None
calculatedPath = None
inCrossing = False
scanRoute = False
qrmessage = ""
currentheading = None
lastCrossing = None
nextCrossing = None
messagelist = list()
lock = threading.Lock()



def QRCapture():
    camera = Camera()
    camera.start_camera()

    global scanRoute
    while True: 

        while scanRoute:
            frame = camera.capture()
            qr_code = vision.find_QR_code(frame)
            message = vision.get_QR_message(qr_code)

            if(message != None and 'example' in messagelist):
                global qrmessage
                qrmessage = message
        camera.close()
        while scanRoute == False:
            print("Kamera ist aus")
        camera.start_camera()




def DriveManager():
    global inCrossing
    global currentheading
    global calculatedPath
    global lastCrossing
    global nextCrossing
    while True:
        if calculatedPath != None and inCrossing == False:
            GoStraight()
            inCrossing == True
            scanRoute == False
            #checkIfAbb
        if calculatedPath != None and inCrossing == True:

            dirnumber = getCrossingDirection()
            #abgleich mit anderem auto

            #lock
            if dirnumber == 0:
                tf.turnLeft
            elif dirnumber == 1:
                tf.turnStraight
            elif dirnumber == 2:
                tf.turnRight
            elif dirnumber == 3:
                tf.turnAround
            currentheading = calculatedPath[0]['direction']
            lastCrossing = calculatedPath[0]['currentCrossing']
            nextCrossing = calculatedPath[0]['nextCrossing']
            calculatedPath.pop(0)
            #lock aufheben
            




            

    


def ServerThread():
    global zumiMap
    zumiMap = gr.Graph()
    zumiMap = pm.initPersonalMap(zumiMap)
    """
    global startDirection
    global startCrossing
    global endCrossing
    """
    global currentheading
    global calculatedPath

    startDirection = 'East'
    startCrossing = 'I'
    endCrossing = 'C'
    currentheading = startDirection
    calculatedPath = zumiMap.CalculatePath(startDirection,startCrossing,endCrossing)


def getCrossingDirection():
    global currentheading
    global calculatedPath
    if currentheading == 'North' and calculatedPath[0]['direction'] == 'West' or currentheading == 'East' and calculatedPath[0]['direction'] == 'North' or currentheading == 'South' and calculatedPath[0]['direction'] == 'East'or currentheading == 'West' and calculatedPath[0]['direction'] == 'South':
        return 0 #left
    elif currentheading == calculatedPath[0]['direction']:
        return 1 #straight
    elif currentheading == 'North' and calculatedPath[0]['direction'] == 'East' or currentheading == 'East' and calculatedPath[0]['direction'] == 'South' or currentheading == 'South' and calculatedPath[0]['direction'] == 'West' or currentheading == 'West' and calculatedPath[0]['direction'] == 'North':
        return 2 #right
    elif currentheading == 'North' and calculatedPath[0]['direction'] == 'South' or currentheading == 'East' and calculatedPath[0]['direction'] == 'West' or currentheading == 'South' and calculatedPath[0]['direction'] == 'North' or currentheading == 'West' and calculatedPath[0]['direction'] == 'East':
        return 3 #turnaround

def GoStraight():
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
        









thread = threading.Thread(target = ServerThread)
thread2 = threading.Thread(target = DriveManager)
#thread3 = threading.Thread()
thread.start()
thread2.start()