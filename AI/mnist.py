#!/usr/bin/python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple, end-to-end, LeNet-5-like convolutional MNIST model example.

This should achieve a test error of 0.7%. Please keep this model as simple and
linear as possible, it is meant as a tutorial for simple convolutional models.
Run with --self_test on the command line to execute a short self-test.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import os
import sys
import time

import numpy
from PIL import Image
import  matplotlib.pyplot as plt
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'
WORK_DIRECTORY = 'data'
IMAGE_SIZE = 28
NUM_CHANNELS = 1
PIXEL_DEPTH = 255
NUM_LABELS = 10
VALIDATION_SIZE = 5000  # Size of the validation set.
SEED = 66478  # Set to None for random seed.
STEP=3
BATCH_SIZE = 35
NUM_EPOCHS = 10
EVAL_BATCH_SIZE = 64
EVAL_FREQUENCY = 100  # Number of steps between evaluations.

Num2label = [[1,0,0,0,0,0,0,0,0,0], #0
             [0,1,0,0,0,0,0,0,0,0], #1
             [0,0,1,0,0,0,0,0,0,0], #2
             [0,0,0,1,0,0,0,0,0,0], #3
             [0,0,0,0,1,0,0,0,0,0], #4
             [0,0,0,0,0,1,0,0,0,0], #5
             [0,0,0,0,0,0,1,0,0,0], #6
             [0,0,0,0,0,0,0,1,0,0], #7
             [0,0,0,0,0,0,0,0,1,0], #8
             [0,0,0,0,0,0,0,0,0,1]  #9 
            ]

def maybe_download(filename):
  """Download the data from Yann's website, unless it's already here."""
  if not tf.gfile.Exists(WORK_DIRECTORY):
    tf.gfile.MakeDirs(WORK_DIRECTORY)
  filepath = os.path.join(WORK_DIRECTORY, filename)
  if not tf.gfile.Exists(filepath):
    print(SOURCE_URL + filename)
    #filepath, _ = urllib.request.urlretrieve(SOURCE_URL + filename, filepath)
    print('filepath is %s' % filepath)
    with tf.gfile.GFile(filepath) as f:
      size = f.Size()
    print('Successfully downloaded', filename, size, 'bytes.')
  return filepath


def extract_data(filename, num_images):
  """Extract the images into a 4D tensor [image index, y, x, channels].

  Values are rescaled from [0, 255] down to [-0.5, 0.5].
  """
  print('Extracting', filename)
  with gzip.open(filename) as bytestream:
    bytestream.read(16)
    buf = bytestream.read(IMAGE_SIZE * IMAGE_SIZE * num_images)
    print(IMAGE_SIZE * IMAGE_SIZE * num_images)
    data = numpy.frombuffer(buf, dtype=numpy.uint8).astype(numpy.float32)
    data1 = numpy.frombuffer(buf, dtype=numpy.uint8).reshape(num_images, IMAGE_SIZE*IMAGE_SIZE)
    '''
    print(data1[0])
    im=data1[12].reshape(28,28)
    fig=plt.figure()
    plotwindow=fig.add_subplot(111)
    plt.imshow(im,cmap='gray')
    plt.show()
    '''
    data = (data - (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH
    data = data.reshape(num_images, IMAGE_SIZE*IMAGE_SIZE)
    #print(data[0])
    return data


             
def extract_labels(filename, num_images):
  """Extract the labels into a vector of int64 label IDs."""
  print('Extracting', filename)
  labels2=[]
  with gzip.open(filename) as bytestream:
    bytestream.read(8)
    buf = bytestream.read(1 * num_images)
    print(num_images)
    labels = numpy.frombuffer(buf, dtype=numpy.uint8).astype(numpy.int64)
    for label in labels :
      labels2.append(Num2label[label])
    print(labels[0:5])
    print(labels2[0:5])
  return labels2


def fake_data(num_images):
  """Generate a fake dataset that matches the dimensions of MNIST."""
  data = numpy.ndarray(
      shape=(num_images, IMAGE_SIZE * IMAGE_SIZE),
      dtype=numpy.float32)
  labels = numpy.zeros(shape=(num_images,10), dtype=numpy.int64)
  print(num_images)
  for image in xrange(num_images):
    label = image % 2
    data[image, :] = label - 0.5
    labels[image] = Num2label[label]
    print("data[%d]" % image,labels[image])
  return data, labels


def error_rate(predictions, labels):
  """Return the error rate based on dense predictions and sparse labels."""
  return 100.0 - (
      100.0 *
      numpy.sum(numpy.argmax(predictions, 1) == labels) /
      predictions.shape[0])

def view_Pic(data, index) :
  print("index is %d" % index)
  disData = data[index]
  os.write(1,"----------------------------")
  for x in xrange(IMAGE_SIZE*IMAGE_SIZE) :
    if disData[x]>0 :
      tempdata="#"
    else :
      tempdata=" "
    if 0 == (x % IMAGE_SIZE) :
      os.write(1,"|\n%s" % (tempdata))
    else :
      os.write(1,"%s" % (tempdata))
  os.write(1,"|\n----------------------------|\n")
  sys.stdout.flush()
  print()
def readAPic(filename, inputnum) :
  im=Image.open(filename,"r")
  x=im.load()
  a=im.getdata()
  Picdata = numpy.ndarray(shape=(1, IMAGE_SIZE * IMAGE_SIZE), dtype=numpy.float32)
  Piclabels = numpy.zeros(shape=(1,10), dtype=numpy.int64)
  for yindex in range(im.size[1]) :
    for xindex in range(im.size[0]) :
      #print(xindex,yindex)
      Picdata[0,yindex*im.size[0]+xindex] = numpy.float32((x[xindex,yindex]- (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH)
  Piclabels[0] = Num2label[int(inputnum)]
  return (Picdata, Piclabels)

def view_A_Pic(data) :
  disData = data
  os.write(1,"----------------------------")
  for x in xrange(IMAGE_SIZE*IMAGE_SIZE) :
    if disData[x]>0 :
      tempdata="#"
    else :
      tempdata=" "
    if 0 == (x % IMAGE_SIZE) :
      os.write(1,"|\n%s" % (tempdata))
    else :
      os.write(1,"%s" % (tempdata))
  os.write(1,"|\n----------------------------|\n")
  sys.stdout.flush()
  print("")


def main( in1 ):  # pylint: disable=unused-argument
  if in1:
    print('Running self-test.')
    train_data, train_labels = fake_data(5)
    #validation_data, validation_labels = fake_data(EVAL_BATCH_SIZE)
    test_data, test_labels = fake_data(5)
    num_epochs = 1
  else:
    # Get the data.
    train_data_filename = maybe_download('train-images-idx3-ubyte.gz')
    train_labels_filename = maybe_download('train-labels-idx1-ubyte.gz')
    test_data_filename = maybe_download('t10k-images-idx3-ubyte.gz')
    test_labels_filename = maybe_download('t10k-labels-idx1-ubyte.gz')

    # Extract it into numpy arrays.
    train_data = extract_data(train_data_filename, 60000)
    train_labels = extract_labels(train_labels_filename, 60000)
    test_data = extract_data(test_data_filename, 10000)
    test_labels = extract_labels(test_labels_filename, 10000)

    # Generate a validation set.
    '''
    validation_data = train_data[:VALIDATION_SIZE, ...]
    validation_labels = train_labels[:VALIDATION_SIZE]
    train_data = train_data[VALIDATION_SIZE:, ...]
    train_labels = train_labels[VALIDATION_SIZE:]
    num_epochs = NUM_EPOCHS
    '''
  train_size = len(train_labels)
  print("len(train_labels) is",len(train_labels))
  print("len(train_data) is",len(train_data))
  print("len(test_labels) is",len(test_labels))
  print("len(test_data) is",len(test_data))

  sess=tf.InteractiveSession()
  x = tf.placeholder("float", shape = [None, IMAGE_SIZE * IMAGE_SIZE])
  y_ = tf.placeholder("float", shape = [None, 10])
  
  W = tf.Variable(tf.zeros([IMAGE_SIZE * IMAGE_SIZE,10]))
  Windata = tf.Variable(tf.zeros([1, IMAGE_SIZE, IMAGE_SIZE, 1]))
  b = tf.Variable(tf.zeros([10]))
  
  sess.run(tf.initialize_all_variables())
  y = tf.nn.softmax(tf.matmul(x, W) + b)
  cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
  
  train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
  
  correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
  calcDigtal = tf.argmax(y,1)
  InputDigtal = tf.argmax(y_,1)
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
  
  tf.scalar_summary("accuracy",accuracy)
  tf.scalar_summary("cross_entropy",cross_entropy)
  
  Windata = tf.reshape(W[:, 0],[1,28,28,1])
  tf.image_summary('W[0]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 1],[1,28,28,1])
  tf.image_summary('W[1]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 2],[1,28,28,1])
  tf.image_summary('W[2]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 3],[1,28,28,1])
  tf.image_summary('W[3]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 4],[1,28,28,1])
  tf.image_summary('W[4]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 5],[1,28,28,1])
  tf.image_summary('W[5]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 6],[1,28,28,1])
  tf.image_summary('W[6]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 7],[1,28,28,1])
  tf.image_summary('W[7]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 8],[1,28,28,1])
  tf.image_summary('W[8]',Windata,max_images=1)
  Windata = tf.reshape(W[:, 9],[1,28,28,1])
  tf.image_summary('W[9]',Windata,max_images=1)
  
  
  
  merged_summary_op = tf.merge_all_summaries()
  os.system("rm -rf /tmp/tensorflow_log/*")
  summary_writer = tf.train.SummaryWriter('/tmp/tensorflow_log/mnist', sess.graph)
  total_step = 0
  add_summary_timer = 0

  #for batchStart in xrange((train_size-BATCH_SIZE)//STEP):
  for batchStart in xrange((train_size-BATCH_SIZE)//STEP):
    batchStart = (batchStart) % (train_size-BATCH_SIZE)
    if 0 == (batchStart % BATCH_SIZE) and 0 != batchStart:
      print("batchStart is",batchStart)
      #print(accuracy.eval(feed_dict={x:test_data, y_:test_labels}))
      summary_str,acc = sess.run([merged_summary_op, accuracy],feed_dict={x:test_data, y_:test_labels})
      add_summary_timer = add_summary_timer + 1
      print('Accuracy atadd_summary_timer%d step %s: %s' % (add_summary_timer, batchStart, acc))
      summary_writer.add_summary(summary_str, add_summary_timer)
    else:
      sess.run(train_step,feed_dict={x:train_data[batchStart*STEP:(batchStart*STEP+BATCH_SIZE-1)], y_:train_labels[batchStart*STEP:(batchStart*STEP+BATCH_SIZE-1)]})
      #summary_writer.add_summary(summary_str, batchStart)
  print("batchStart is",batchStart)
  #print(accuracy.eval(feed_dict={x:test_data, y_:test_labels}))
  summary_str,acc = sess.run([merged_summary_op, accuracy],feed_dict={x:test_data, y_:test_labels})
  add_summary_timer = add_summary_timer + 1
  print('Accuracy atadd_summary_timer%d step %s: %s' % (add_summary_timer, batchStart, acc))
  summary_writer.add_summary(summary_str, add_summary_timer)
  
  CALC_TIME=50
  print(sess.run([calcDigtal, InputDigtal],feed_dict={x:test_data[0:CALC_TIME], y_:test_labels[0:CALC_TIME]}))
  
  print("Enter Command Line Mode")
  while True:
    indata = raw_input('%%')
    if "q" == indata:
      break;
    elif "d" == indata.split()[0] :
      print(indata.split())
      if not indata.split()[1].isdigit() :
        print("Pls input d + space + digit,example: d 4")
        continue
      view_Pic(test_data, int(indata.split()[1]))
    elif "t" == indata.split()[0] :
      (Picdata,Piclabels) = readAPic("./pic/"+indata.split()[1]+".bmp", indata.split()[1])
      #print(Picdata,Piclabels)
      WResult, yResult, calcDigtalnum, InputDigtalNum = sess.run([W, y, calcDigtal, InputDigtal], feed_dict={x:Picdata, y_:Piclabels})
      view_A_Pic(Picdata[0])
      print("calcDigtalnum is ", calcDigtalnum[0])
      print("y is ", yResult)
      #for index in range(10) :
        #print("W[%d] is " % index, WResult[:,index])
    else :
      continue
  sess.close()

if __name__ == '__main__':
  main(False)
  
