import numpy as np
import os
import sys
import tensorflow as tf

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import urllib, cStringIO

from utils import label_map_util
from utils import visualization_utils as vis_util

import io
import socket
import struct

PATH_TO_CKPT='/home/hoyong/tensorflow/models/research/od_model_test/ssd/frozen_inference_graph.pb'
PATH_TO_LABELS ='/home/hoyong/tensorflow/models/research/object_detection/data/mscoco_label_map.pbtxt'

NUM_CLASSES=90 

#detection_graph = None
#category_index = None

def setConnection(ip, port):
  client_socket = socket.socket()
  client_socket.connect((ip, port))

  connection = client_socket.makefile('wb')

  return client_sock, connection

def main():
  cnt = 0
  detection_graph = loadModel()
  category_index = loadLabelMap()
  ip = '192.168.43.107'
  port = 8666
  cnt = getImage(ip, port, 'front', cnt, detection_graph, category_index)

def loadModel():
  # load a (frozen) Tensorflow model into memory
  # global detection_graph
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')

  print "==== Load a Tensorflow model into memory===="
  return detection_graph

def loadLabelMap():
  # loading label map
  # global category_index
  label_map  = label_map_util.load_labelmap(PATH_TO_LABELS)
  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
  category_index = label_map_util.create_category_index(categories)

  return category_index

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

def objectDetection(image, cnt, direction, detection_graph, category_index):
  #detection
  #global detection_graph
  #global category_index

  # Size, in inches, of the output images
  IMAGE_SIZE = (12, 8)

  with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
      # Definite input and output Tensors for detection_graph
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected
      detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects
      # Score is shown on the result image, together with the class label
      detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
      detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # the array based representation of the image will be used later in order to prepare the result image with boxed and labels on it
      image_np = load_image_into_numpy_array(image)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection
      (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict={image_tensor:image_np_expanded})
      temp_image, box_class = vis_util.visualize_boxes_and_labels_on_image_array(image_np, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores), category_index, use_normalized_coordinates=True, line_thickness=8)
      fig = plt.figure(figsize=IMAGE_SIZE)
      plt.imshow(image_np)
      #plt.show()
      fig.savefig('./' + direction + '/' + str(cnt) + '.jpg')
      print "Success"
      for box, class_name in box_class.items():
        print "========================================"
        print class_name
        print box
        print "========================================"

def getImage(ip, port, direction, cnt, detection_graph, category_index):
  # global cnt
  URL = 'http://' + ip + ':' + str(port) + '/?action=snapshot'

  f = cStringIO.StringIO(urllib.urlopen(URL).read())
  img = Image.open(f)

  objectDetection(img, cnt, direction, detection_graph, category_index)

  cnt += 1
  return cnt

if __name__=="__main__":
  main()
