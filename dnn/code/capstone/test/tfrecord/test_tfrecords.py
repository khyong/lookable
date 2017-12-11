import tensorflow as tf
from utils import dataset_util
import os
from PIL import Image

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

PATH = './shoes'

def main(_):
  writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

  files = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
  pictures = getImageInfo(files)
  for p in pictures:
    print p
    name, xmins, xmaxs, ymins, ymaxs = p
    tf_example = create_tf_example(name, xmins, xmaxs, ymins, ymaxs)
    writer.write(tf_example.SerializeToString())
  writer.close()

def getImageInfo(files):
  fr = open('./coor.txt', 'rb')

  pictures = []

  cnt = 0
  for line_orig in fr:
    line = line_orig[:len(line_orig)-2]
    if cnt == 0:
      if not line in files:
        continue
      else:
        name = line
    else:
      tokens = line.split(',')
      if cnt == 1:
        xmins = float(tokens[0])
        ymins = float(tokens[1])
      elif cnt == 2:
        xmaxs = float(tokens[0])
        ymaxs = float(tokens[1])
    cnt += 1
    if cnt % 3 == 0:
      pictures.append((name, xmins, xmaxs, ymins, ymaxs))
      cnt = 0
  fr.close()
  return pictures

def create_tf_example(ex_name, ex_xmins, ex_xmaxs, ex_ymins, ex_ymaxs):
  # TODO(user): Populate the following variables from your example.
  image = Image.open(os.path.join(PATH, ex_name))
  width, height = image.size
  '''
  height = ex_height # Image height
  width = ex_width # Image width
  '''
  filename = ex_name # Filename of the image. Empty if image is not from file
  encoded_image_data = image.tobytes() # Encoded image bytes
  image_format = b'jpg' # b'jpeg' or b'png'

  xmins = [ex_xmins] # List of normalized left x coordinates in bounding box (1 per box)
  xmaxs = [ex_xmaxs] # List of normalized right x coordinates in bounding box
             # (1 per box)
  ymins = [ex_ymins] # List of normalized top y coordinates in bounding box (1 per box)
  ymaxs = [ex_ymaxs] # List of normalized bottom y coordinates in bounding box
             # (1 per box)
  classes_text = ['Shoes'] # List of string class name of bounding box (1 per box)
  classes = [91] # List of integer class id of bounding box (1 per box)

  tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_image_data),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
  }))
  return tf_example

if __name__=="__main__":
  tf.app.run()
