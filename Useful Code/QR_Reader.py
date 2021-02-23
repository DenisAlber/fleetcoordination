from zumi.zumi import Zumi
from zumi.util.camera import Camera
from zumi.util.vision import Vision 

zumi = Zumi()
zumi.reset_gyro()
speed = 30
heading = 0
camera = Camera()
vision = Vision()
camera.start_camera()
for x in range(40): # Take steps
    frame = camera.capture()
    qr_code = vision.find_QR_code(frame)
    message = vision.get_QR_message(qr_code)

    if message != None:
        camera.close()
        print(message)
        zumi.stop()
        break
    
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