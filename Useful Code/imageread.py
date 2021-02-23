from zumi.zumi import Zumi
from zumi.util.screen import Screen
import cv2 as cv
import time 
from zumi.util.vision import Vision # New library!
from zumi.util.camera import Camera # New library!
import numpy as np
from matplotlib import pyplot as plt

zumi = Zumi()
camera = Camera()
screen = Screen()
vision = Vision()


camera.start_camera()
img = camera.capture()
camera.close()
gray = vision.convert_to_gray(img) # Convert it to gray




edges = cv.Canny(gray,100,200)
camera.show_image(edges)
"""
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
"""