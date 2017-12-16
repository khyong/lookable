import main_object_detection as od
import threading

IP_PI = ['192.168.43.107', '192.168.43.204', '192.168.43.62']
DIRECTION = ['front', 'diag', 'down']
PORT_PI = 8666
#PORT_ULTRA = 10100
#PORT_GEO = 10200

def main():
  cnt = 0
  detection_graph = od.loadModel()
  category_index = od.loadLabelMap()
  cnt = connectPI(1, cnt, detection_graph, category_index)
  #sock_2, con_2 = connectPI(2)
  #sock_3, con_3 = connectPI(3)
  #t1 = threading.Thread(target=od.getImage, args=(sock_1, con_1, 'front'))
  #t2 = threading.Thread(target=od.getImage, args=(sock_2, con_2, 'diag'))
  #t3 = threading.Thread(target=od.getImage, args=(sock_3, con_3, 'down'))

  #t1.start()
  #t2.start()
  #t3.start()

def connectPI(pi_num, cnt, detection_graph, category_index):
  ip = IP_PI[pi_num-1]
  direction = DIRECTION[pi_num-1]
  cnt = od.getImage(ip, PORT_PI, direction, cnt, detection_graph, category_index)
  print "[pi " + str(pi_num) + "] connected"
  return cnt

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
