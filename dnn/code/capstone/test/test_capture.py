from PIL import Image
import urllib, cStringIO
import cv2
import time

URL = 'http://192.168.43.204:8666/?action=snapshot'

while True:
  f = cStringIO.StringIO(urllib.urlopen(URL).read())
  img = Image.open(f)
  cv2.imwrite('../file_test/test.jpg', img)
  img.close()
  time.sleep(1)
