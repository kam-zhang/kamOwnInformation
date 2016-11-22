#!/usr/bin/python
#-*—coding:utf-8-*-

import struct
import os
import sys
import numpy as np
import  matplotlib.pyplot as plt
from PIL import Image
# bin file input
filename="./MNIST_data/train-images-idx3-ubyte"
binfile=open(filename,'rb')
buf=binfile.read()
# bigend read 4 unsigned int32
#struct  http://www.cnblogs.com/gala/archive/2011/09/22/2184801.html

index=0
magic,numImages,numRows,numColumns=struct.unpack_from('>IIII',buf,index)
index+=struct.calcsize('>IIII')
if not os.path.exists("./MNIST_data/train") :
    os.mkdir("./MNIST_data/train")
os.system("rm -f ./MNIST_data/train/*.bmp")

numImages = 100
for image in range(0,numImages):
    im=struct.unpack_from('>784B',buf,index)
    index+=struct.calcsize('>784B')

    im=np.array(im,dtype='uint8')
    im=im.reshape(28,28)
   # fig=plt.figure()
   # plotwindow=fig.add_subplot(111)
   # plt.imshow(im,cmap='gray')
   # plt.show()
    im=Image.fromarray(im)
    im.save("./MNIST_data/train/train_%d.bmp" % (image),'bmp')
    
binfile.close()
