import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.10.101'
port = 9999

s.connect((host, port))

while True:
	send_data = raw_input()
	s.send(send_data)
	print "[SEND] " + str(send_data)
	recv_data = s.recv(1024)
	recv_low = str(recv_data).lower()
	if recv_low == "exit":
		print "Server closed"
		break
	elif recv_low != "again":
		print "Distance: " + str(recv_data)
s.close()
