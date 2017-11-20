import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

data_path = '../tfrecord/many2one.tfrecords' # address to save the hdf5 file

with tf.Session() as sess:
  feature = {'image': tf.FixedLenFeature([], tf.string), 'label': tf.FixedLenFeature([], tf.int64)}

  # create a list of filenames and pass it to a queue
  filename_queue = tf.train.string_input_producer([data_path], num_epochs=1)

  # define a reader and read the next record
  reader = tf.TFRecordReader()
  _, serialized_example = reader.read(filename_queue)

  # decode the record read by the reader
  features = tf.parse_single_example(serialized_example, features=feature)

  # convert the image data from string back to the numbers
  images = tf.decode_raw(features['image'], tf.float32)

  # cast label data into int32
  labels = tf.cast(features['label'], tf.int32)

  # Reshape image data into the original shape
  images = tf.reshape(images, [224, 224, 3])

  # Initialize all global and local variables
  init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
  sess.run(init_op)

  # create a coordinator and run all QueueRunner objects
  coord = tf.train.Coordinator()
  threads = tf.train.start_queue_runners(coord=coord)

  for i in range(12):

    img, lbl = sess.run([images, labels])

    img = img.astype(np.uint8)

    #plt.plot(224,224)
    plt.imshow(img)
    plt.title('bollard' if lbl==0 else 'bench')
    plt.show()

  # stop the threads
  coord.request_stop()

  # wait for threads to stop
  coord.join(threads)
  sess.close()
