#import io
from picamera.array import PiRGBArray
import picamera
import cv2
from time import sleep
#from PIL import Image

camera = picamera.PiCamera()
rawCapture = PiRGBArray(camera)

#stream = io.BytesIO()

#camera.start_preview()

camera.capture(rawCapture, format='bgr')

img = rawCapture.array

cv2.imwrite('test.png', img)

print(img.shape[:2])

camera.stop_preview()

camera.close()

#camera.start_recording('camera.h264')
#sleep(60)
#camera.stop_recording()
