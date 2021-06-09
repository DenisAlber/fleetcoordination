from zumi.zumi import Zumi
from zumi.util.camera import Camera
from zumi.util.vision import Vision

camera = Camera()
vision = Vision()

camera = Camera()
camera.start_camera()
frame = camera.capture()
camera.close()
qr_code = vision.find_QR_code(frame)
message = vision.get_QR_message(qr_code)
print(message)