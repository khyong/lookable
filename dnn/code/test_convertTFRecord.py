import tensorflow as tf
import numpy as np
import cv2

image_path = '../../../object_detection/test_images/image1.jpg'

# load images
def load_image(addr):
  # read an image and resiez to (224, 224)
  # cv2 load images as BGR, convert it to RGB
  img = cv2.imread(addr)
  img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_CUBIC)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = img.astype(np.float32)
  return img

# convert data to features
def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# write data inte a TFRecords file
train_filename = 'train.tfrecords'

# open the TFRecords file
writer = tf.python_io.TFRecordWriter(train_filename)

img = load_image(image_path)

feature = {'train/image': _bytes_feature(tf.compat.as_bytes(img.tostring()))}

# create an example protocol buffer
example = tf.train.Example(features=tf.train.Features(feature=feature))

# Serialize to string and write on the file
writer.write(example.SerializeToString())

writer.close()
