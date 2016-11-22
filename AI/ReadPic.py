#!/usr/bin/python
#-*—coding:utf-8-*-

import struct
import os
import sys
import numpy as np
import  matplotlib.pyplot as plt
from PIL import Image

IMAGE_SIZE = 28
PIXEL_DEPTH = 255

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

im=Image.open("./pic/"+sys.argv[1]+".bmp","r")
x=im.load()
a=im.getdata()
data=[]
for yindex in range(im.size[1]) :
  for xindex in range(im.size[0]) :
    #print(xindex,yindex)
    data.append((x[xindex,yindex]- (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH)
#data = (data - (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH
#data = data.reshape(num_images, IMAGE_SIZE*IMAGE_SIZE)
print len(data)
view_A_Pic(data)


