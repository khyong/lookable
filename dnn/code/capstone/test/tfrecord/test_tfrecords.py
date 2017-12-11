import tensorflow as tf
from utils import dataset_util
import os
from PIL import Image

'''
flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS
'''

PATH = './shoes'

def main():
  #writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

  files = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
  pictures = getImageInfo(files)
  for p in pictures:
    print p

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
        image = Image.open(os.path.join(PATH, line));
        width, height = image.size
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
      pictures.append((name, width, height, xmins, xmaxs, ymins, ymaxs))
      cnt = 0
  fr.close()
  return pictures

if __name__=="__main__":
  main()
