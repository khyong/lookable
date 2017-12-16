import numpy as np
import os
import sys
import tensorflow as tf
from multiprocessing import Pool

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
import time
import cv2

PATH_TO_CKPT='/home/hoyong/tensorflow/models/research/od_model_test/ssd/frozen_inference_graph.pb'
PATH_TO_LABELS ='/home/hoyong/tensorflow/models/research/object_detection/data/mscoco_label_map.pbtxt'

NUM_CLASSES=90

def main():
  detection_graph = loadModel()
  category_index = loadLabelMap()
  cnt = 0
  ip = ''
  port = 8666
  start = time.time()
  getImage(ip, port, 'front', cnt, detection_graph, category_index)
  end = time.time()
  print end - start

def loadModel():
  # load a (frozen) Tensorflow model into memory
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    fid = tf.gfile.GFile(PATH_TO_CKPT, 'rb')
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

  print "==== Load a Tensorflow model into memory===="
  return detection_graph

def loadLabelMap():
  # loading label map
  label_map  = label_map_util.load_labelmap(PATH_TO_LABELS)
  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
  category_index = label_map_util.create_category_index(categories)

  return category_index

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

def objectDetection(image, cnt, direction, detection_graph, category_index):
  #detection
  # Size, in inches, of the output images
  IMAGE_SIZE = (12, 8)

  sess = tf.Session(graph=detection_graph)
  # Each box represents a part of the image where a particular object was detected
  detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
  # Each score represent how level of confidence for each of the objects
  # Score is shown on the result image, together with the class label
  detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
  detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
  num_detections = detection_graph.get_tensor_by_name('num_detections:0')
  # Definite input and output Tensors for detection_graph
  image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
  # the array based representation of the image will be used later in order to prepare the result image with boxed and labels on it
  image_np = load_image_into_numpy_array(image)
  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
  image_np_expanded = np.expand_dims(image_np, axis=0)
  s = time.time()
  boxes, scores, classes, num = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict={image_tensor:image_np_expanded})
  e = time.time()
  # Actual detection
  #s = time.time()
  _, box_class = vis_util.visualize_boxes_and_labels_on_image_array(image_np, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores), category_index, use_normalized_coordinates=True, line_thickness=8)
  #e = time.time()
  print str(e-s)
  return box_class.items()

def getImage(ip, port, direction, cnt, detection_graph, category_index):
  #URL = 'http://' + ip + ':' + str(port) + '/?action=snapshot'

  img = Image.open('/home/hoyong/tensorflow/models/research/object_detection/test_images/image1.jpg')

  box_items = objectDetection(img, cnt, direction, detection_graph, category_index)

  cnt += 1
  return cnt, box_items

if __name__=="__main__":
  main()

