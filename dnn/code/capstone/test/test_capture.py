from PIL import Image
import urllib, cStringIO
import cv2
import time
import numpy as np

URL = 'http://192.168.43.204:8666/?action=snapshot'

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

while True:
  f = cStringIO.StringIO(urllib.urlopen(URL).read())
  img = Image.open(f)
  img_np = load_image_into_numpy_array(img)
  cv2.imwrite('../file_test/test.jpg', img_np)
  img.close()
  print "  Complete"
  time.sleep(1)
