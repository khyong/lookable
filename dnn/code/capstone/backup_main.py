import main_object_detection as od
import threading

IP = '0.0.0.0'

PORT_PI = [9100, 9200, 9300]
PORT_ULTRA = 10100
PORT_GEO = 10200

def main():
  od.loadModel()
  od.loadLabelMap()
  sock_1, con_1 = connectPI(1)
  sock_2, con_2 = connectPI(2)
  sock_3, con_3 = connectPI(3)
  t1 = threading.Thread(target=od.getImage, args=(sock_1, con_1, 'front'))
  t2 = threading.Thread(target=od.getImage, args=(sock_2, con_2, 'diag'))
  t3 = threading.Thread(target=od.getImage, args=(sock_3, con_3, 'down'))

  t1.start()
  t2.start()
  t3.start()

def connectPI(pi_num)
  port = PORT_PI[pi_num-1]
  client_sock, connection = od.setConnection(IP, port)
  return client_sock, connection

# android

# object detection


# web

# threading
'''
import threading

def sum(low, high):
    total = 0
    for i in range(low, high):
        total += i
    print "Subthread" + str(total)

t = threading.Thread(target=sum, args=(1,100))
t.start()

print "Main Thread"
'''

if __name__=="__main__":
  main()
