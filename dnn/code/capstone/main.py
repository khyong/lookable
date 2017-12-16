import main_object_detection as od
import threading
import time

IP_PI = ['192.168.43.107', '192.168.43.204', '192.168.43.62']
CNT_PI = [0, 0, 0]
DIRECTION = ['front', 'diag', 'down']
PORT_PI = 8666
#PORT_ULTRA = 10100
#PORT_GEO = 10200

start = 0
def main():
  global start
  detection_graph = od.loadModel()
  category_index = od.loadLabelMap()
  start = time.time()
  while True:
    CNT_PI[0] = getPiImage(0, CNT_PI[0], detection_graph, category_index)
    #CNT_PI[1] = getPiImage(1, CNT_PI[1], detection_graph, category_index)
    #CNT_PI[2] = getPiImage(2, CNT_PI[2], detection_graph, category_index)

def getPiImage(pi_num, cnt, detection_graph, category_index):
  global start
  ip = IP_PI[pi_num]
  direction = DIRECTION[pi_num]
  cnt, box_items = od.getImage(ip, PORT_PI, direction, cnt, detection_graph, category_index)
  end = time.time()
  for box, class_name in box_items:
    print "========================================"
    print class_name
    print box
    print "========================================"
  print "  [" + str(end-start) + "][pi " + str(pi_num) + "] capture the image"
  return cnt

if __name__=="__main__":
  main()
