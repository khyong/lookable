import socket
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.199.134'
port = 8888

serversocket.bind((host, port))

serversocket.listen(5)

clientsocket, addr = serversocket.accept()
print "Got a connection from %s" % str(addr)

while True:
    recv_data = clientsocket.recv(1024)
    print "[RECV] " + str(recv_data)
    currentTime = time.ctime(time.time())
    clientsocket.send(currentTime.encode('ascii'))
    time.sleep(1)
clientsocket.close()
