#!/bin/python
# -*- coding: utf-8 -*-

import time
import threading
import sys
import os

global runtime

def lop1():
    global runtime
    while True :
        print raw_input(">>")
        runtime = 0

runtime = 0
t1=threading.Thread(target=lop1)
t1.setDaemon(True)
t1.start()
while True :
    if 3 < runtime :
        #os.kill(t1)
        exit()
    else :
        runtime = runtime + 1;
    time.sleep(1)
    print "Lop1 runtime is %d" % (runtime)

#t1.join()

    
