import urllib, cStringIO
from PIL import Image

URL = 'http://192.168.43.107:8666/?action=snapshot'

f = cStringIO.StringIO(urllib.urlopen(URL).read())
img = Image.open(f)
img.show()
