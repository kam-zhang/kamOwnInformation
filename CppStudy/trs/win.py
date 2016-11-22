#!/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from socket import *
import time
import struct
import os
import sys
import commands
from PIL import Image
import threading

# Address and Port
ClientHOST = ''
ServerHOST = '10.92.234.34'
PORT = 21218
ClientADDR = (ClientHOST, PORT)
ServerADDR = (ServerHOST, PORT)

# BuffSize
BUFSIZ = 4096
DAT_HEAD_LEN = 12

# 4×Ö½Ú:msgtype£»4×Ö½Ú:index£»4×Ö½Ú:len£»data...
# msgtype=100,·¢ËÍÎÄ¼þ´óÐ¡ºÍÎÄ¼þÃû×Ö£¬ indexÎªÎÄ¼þ´óÐ¡£¬lenÎªÎÄ¼þÃû³¤¶È£¬dataÎªÎÄ¼þÃû³Æ
# msgtype=200,·¢ËÍÊý¾Ý£¬ indexÎª0~pkgnum£¬lenÎªÊý¾Ý³¤¶È£¬dataÎªÊý¾Ý
# msgtype=300,¶Ï¿ªÁ¬½Ó£¬serverºÍclient¶¼Á¬½Ó

def trsLog(logstr) :
    #print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + " " + logstr
    a=1

def view_bar(num=1, sum=100, bar_word="="):
    if 0 == sum :
        num =1
        sum =1
    rate = float(num) / float(sum)
    rate_num = rate * 100
    buffer = "|"
    for i in range(0, int(100/5)):
        if i < int(rate_num/5) :
            buffer += bar_word
        else:
            buffer += " "
    buffer += "| "
    os.write(1, buffer)
    os.write(1, '%2.2f%%:' %(rate_num))
    os.write(1,"\r")
    sys.stdout.flush()
RcvFileCount = 0
STUDY_PIC_NUM = 10
studyresult = None
oldpic = None
samePiccounter = 0
def RevOneDataPack(tcp, expectIndex, expectRcvLen) :
    data = ""
    while True :
        data += tcp.recv(BUFSIZ)
        if 0 == len(data) :
            trsLog("Receive Error")
            return (msgtype,Rcvindex,0,data)
        (msgtype,Rcvindex,rcvlen) = struct.unpack("3I",data[0:DAT_HEAD_LEN])
        #trsLog("msgtype[%d], Rcvindex[%d],rcvlen[%d],datalen[%d]" % (msgtype,Rcvindex,rcvlen,len(data)))
        if (200 != msgtype) or (Rcvindex != expectIndex) or (expectRcvLen != rcvlen)  or ((expectRcvLen + DAT_HEAD_LEN) != len(data)):
            #trsLog("Receive Msg Error,ReRecive")
            continue
        else:
            break
    tcp.send("ACK")
    (rcvdata,)=struct.unpack("%ds" % (rcvlen), data[DAT_HEAD_LEN:(DAT_HEAD_LEN+rcvlen)])
    return (msgtype,Rcvindex,rcvlen,rcvdata)
def calcres(im1,im2) :
		res = 0
		imm1=im1
		a=imm1.load()
		b=im2.load()
		for yindex in range(imm1.size[1]) :
				for xindex in range(imm1.size[0]) :
						#print(a[xindex,yindex])
						temp= (a[xindex,yindex][0] - b[xindex,yindex][0])
						res += temp * temp
		return res/1000000


def RecOneFile(tcp, filename, filelen):
    global RcvFileCount
    global studyresult
    global oldpic
    global samePiccounter
    trsLog("%s size is %d bytes" % (filename,filelen))
    pkgnum=filelen/(BUFSIZ-DAT_HEAD_LEN)
    lastpkgsize = filelen%(BUFSIZ-DAT_HEAD_LEN)
    trsLog("pkgnum is %d, lastpkgsize is %d" % (pkgnum, lastpkgsize))
    rcvFilepath=os.path.join(".","rcvFile")
    #print("rcvFilepath is %s" % (rcvFilepath))
    if(not os.path.exists(rcvFilepath)) :
        os.makedirs(rcvFilepath)
    rcvFileName=os.path.join(rcvFilepath,filename)
    #print("rcvFileName is %s" % (rcvFileName))
#    if os.path.exists(rcvFileName) :
#        rcvFileName = rcvFileName + "%f" % (time.time())
    #print("rcvFileName2 is %s" % (rcvFileName))
    fd=open(rcvFileName,"wb")
    for index in range(pkgnum) :
        (msgtype,Rcvindex,rcvlen,rcvdata) = RevOneDataPack(tcp, index, BUFSIZ-DAT_HEAD_LEN)
        if 0 == rcvlen :
            fd.close()
            return 
        fd.write(rcvdata)
       # if 0 == (index % 300) :
            #view_bar(index, pkgnum)
        #trsLog("write file OK")
    if 0 != lastpkgsize :
        (msgtype,Rcvindex,rcvlen,rcvdata) = RevOneDataPack(tcp, pkgnum, lastpkgsize)
        if 0 == rcvlen :
            fd.close()
            return 
        fd.write(rcvdata)
        #view_bar(pkgnum, pkgnum)
    #print ""
    trsLog("write file OK")
    trsLog('Receive \"%s\"[len:%d] successful\n' % (filename, filelen))
    fd.close()
    ff=os.path.splitext(rcvFileName)
    if '.gif' != ff[1] :
        temp=Image.open(rcvFileName,'r')
        temp.load()
        temp.save(ff[0]+'.gif')
        #print('covert %s to %s'%(rcvFileName, ff[0]+'.gif'))
        updatelabelPic(ff[0]+'.gif')
    else:
        updatelabelPic(rcvFileName)
    temp = Image.open(rcvFileName,'r')
    if RcvFileCount < STUDY_PIC_NUM :
        if studyresult == None :
            studyresult = temp
        else :
            studyresult = Image.blend(temp, studyresult, 0.5)
        samePiccounter = 0
    else :
        chayizhi = calcres(temp, studyresult)
        print 'chayizhi is ',chayizhi
        if chayizhi > 300 :
            ff=os.path.splitext(rcvFileName)
            timestruct=time.localtime()
            temp2="%4d%02d%02d_%02d%02d%02d" % (timestruct.tm_year,timestruct.tm_mon,timestruct.tm_mday,timestruct.tm_hour,timestruct.tm_min,timestruct.tm_sec)
            if(not os.path.exists(".\\MonitorImage")) :
                os.makedirs(".\\MonitorImage")
            newfilename = ".\\MonitorImage\\MovingImage" + "_" + temp2 + ff[1]
            os.system('copy %s %s' % (rcvFileName,newfilename))
            print 'save file :',newfilename
        chayizhi = calcres(temp, oldpic)
        if chayizhi < 200 :
            samePiccounter += 1
            if 20 <= samePiccounter :
                RcvFileCount = 0
                studyresult = None
    RcvFileCount += 1
    oldpic = temp
def rcvInfo( tcp ) :
    data = tcp.recv(BUFSIZ)
    #trsLog "receive data %s" % (data)
    return data

def server(ADDR):
    # build socket
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    # bind socket
    tcpSerSock.bind(ADDR)
    # listen 5 client 
    tcpSerSock.listen(5)
    CurrendPath = "~"

    while True:
        print "\n"
        trsLog('waiting for connection...')
        # build client socket
        tcpCliSock, addr = tcpSerSock.accept()
        trsLog('...connect from:' + str(addr))
        CurrendPath = "."
        # accept data and process
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if 0 == len(data) :
                trsLog("Receive Error")
                break
            (msgtype,index,datalen) = struct.unpack("3I",data[0:DAT_HEAD_LEN])
            info=""
            if 0 != datalen :
                (info,) = struct.unpack("%ds" % datalen,data[DAT_HEAD_LEN:(DAT_HEAD_LEN+datalen)])
            print "\n"
            trsLog("msgtype[%d], index[%d],datalen[%d] data:%s" % (msgtype,index,datalen,info))
            if 100 == msgtype :
                tcpCliSock.send("ACK")
                time.sleep(0.01)
                filename=data[DAT_HEAD_LEN:DAT_HEAD_LEN+datalen]
                RecOneFile(tcpCliSock, filename, index)
            elif 200 == msgtype :
                tcpCliSock.send("ACK")
                time.sleep(1)
                cmd="ls -a %s" % CurrendPath
                trsLog("cmd:"+ cmd)
                status, output = commands.getstatusoutput(cmd)
                tcpCliSock.send(output)
            elif 201 == msgtype :
                tcpCliSock.send("ACK")
                time.sleep(1)
                tcpCliSock.send(CurrendPath)
            elif 202 == msgtype :
                tcpCliSock.send("ACK")
                trsLog(info+"\n")
                time.sleep(1)
                if '~' == info.split()[1][0] or '/' == info.split()[1][0] :
                    CurrendPath = info.split()[1]
                else :
                    CurrendPath = CurrendPath + '/' + info.split()[1]
                trsLog("CurrendPath:"+CurrendPath)
                tcpCliSock.send(CurrendPath)
            elif 203 == msgtype :
                tcpCliSock.send("ACK")
                filename=CurrendPath + '/' + info.split()[1]
                trsLog("filename:"+filename)
                time.sleep(1)
                if not os.path.exists(filename): 
                    trsLog("\"%s\" is not exists!!!" % (filename))
                    sendOnePkg(tcpCliSock, 0xff, 0,0, "")
                else :
                    sendOneFile(tcpCliSock, filename)
            elif 300 == msgtype:
                tcpCliSock.send("ACK")
                trsLog("close this connect:"+str(addr)+"\n")
                time.sleep(1)
                break
            else :
                trsLog("msgtype[%d] Receive Error" % msgtype)
        # close client socket 
        tcpCliSock.close()
    tcpSerSock.close()



picpath='./'
counter = 0
img = None
lab = None
#filename = None
def updatePic():
    global counter
    if(counter==0):
        counter = 1
    else:
        counter += 1
        if(8==counter):counter = 1

    pic= picpath + "%d"%counter +'.gif'
    print "pic is %s" % pic
    return pic
def updatelabelPic(filename):
    global img
    global lab
#    global filename
    print "lab image is ", lab['image'],"filename is ",filename
    img = PhotoImage(file=filename)
    lab['image'] = img
 #   filename = updatePic()
#    lab.after(1000, func=updatelabelPic)

def initWin():
    global img
    global lab
    win = Tk()
    win.title('Hello')
    #win.geometry('200x200+300+300')
    lab = Label(win, image=img)
    lab.pack()
    return win

def StartServer():
    server(('',PORT))

t1=threading.Thread(target=StartServer)
t1.setDaemon(True)
t1.start()


win = initWin()
#time.sleep(1)
#filename = updatePic()
#lab.after(1000, func=updatelabelPic)
print "enter mainloop"
win.mainloop()

