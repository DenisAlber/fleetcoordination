import requests
import json
import threading
import time

from zumi.zumi import Zumi
from zumi.util.camera import Camera
from zumi.util.vision import Vision

stopCar = False
lock = threading.Lock()


IRB = 120
speed = 30
zumi = Zumi()
camera = Camera()
vision = Vision()

def QRCodeTaker():
    camera = Camera()
    camera.start_camera()
    while True:
        
      
        frame = camera.capture()
    
        
        qr_code = vision.find_QR_code(frame)
        message = vision.get_QR_message(qr_code)
        print(message)
        global stopCar
        if(message != None):
            
            stopCar = True
            zumi.stop()
            camera.close()
            print("ALARMALARMALARMALARM")
        if(stopCar == True):
            print("Denis stinkt")


def drive():
    heading = 0
    zumi.reset_gyro()
    for x in range(2000): # Take steps
        
        global stopCar
        if(stopCar == True):
            break

        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]

        if bottom_right_ir > IRB and bottom_left_ir > IRB:
            heading = heading           # do nothing
            
        elif bottom_left_ir < IRB and bottom_right_ir < IRB and x > 10:
            break
    
            
        elif bottom_right_ir < IRB:
            heading += 0.5              # turn left
            
        elif bottom_left_ir < IRB:
            heading -= 0.5               # turn right
            
        
        zumi.go_straight(speed, heading)
    zumi.stop()


thread = threading.Thread(target = QRCodeTaker)
thread2 = threading.Thread(target = drive)
thread.start()
thread2.start()

print("wait...")