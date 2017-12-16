import io
import socket
import struct
from PIL import Image
import numpy
import os
import time

client_socket=socket.socket()
client_socket.connect(('192.168.43.204',9999))

connection=client_socket.makefile('wb')
count=0
try:
    start = time.time()
    while True:
        image_len=struct.unpack('<L',connection.read(4))[0]
        if not image_len:
            break

        image_stream=io.BytesIO()
        image_stream.write(connection.read(image_len))

        #if count == 100:
        #    count = 0
        delay = time.time() - start
        image_stream.seek(0)
        image=Image.open(image_stream)
        print('Image is %dx%d' % image.size)
        temp_file = '/var/www/html/img/front/' + str(count)+'.jpg'
        image.save(temp_file,'JPEG')
        image.verify()
        print('Image is verified')
        print "[Delay] " + str(delay)
        #count+=1

finally:
    connection.close()
    client_socket.close()
