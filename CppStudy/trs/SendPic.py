#!/bin/python
# -*- coding: utf-8 -*-

from socket import *
import time
import struct
import os
import sys
import commands
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

# 4字节:msgtype；4字节:index；4字节:len；data...
# msgtype=100,发送文件大小和文件名字， index为文件大小，len为文件名长度，data为文件名称
# msgtype=200,发送数据， index为0~pkgnum，len为数据长度，data为数据
# msgtype=300,断开连接，server和client都连接

def trsLog(logstr) :
    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + " " + logstr

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

def rcvInfo( tcp ) :
    data = tcp.recv(BUFSIZ)
    #trsLog "receive data %s" % (data)
    return data

def sendOnePkg(tcp, msgtype, index, len, data) :
    format = "3I%ds" % len
    senddata=struct.pack(format,msgtype,index,len,data)
    if struct.calcsize(format) > BUFSIZ:
        trsLog("len_senddata[%d] > BUFSIZ[%d]" % (struct.calcsize(format), BUFSIZ))
        return 0
    n=tcp.send(senddata)
    #trsLog("sendOnePkg:msgtype[%d],index[%d],len[%d],send %d bytes" % (msgtype, index, len, n))
    Rsp=rcvInfo(tcp)
    if not "ACK" == Rsp :
        trsLog("Rsp[%s] is Error" % (Rsp))
        return 0
    #trsLog("send successful")
    return n

def sendOneFile(tcp, input) :
    sizeoffile=os.path.getsize(input)
    trsLog("%s size is %d bytes" % (input,sizeoffile))
    pkgnum=sizeoffile/(BUFSIZ-DAT_HEAD_LEN)
    lastpkgsize = sizeoffile%(BUFSIZ-DAT_HEAD_LEN)
    trsLog("pkgnum is %d, lastpkgsize is %d" % (pkgnum, lastpkgsize))
    fd=open(input, "rb")
#filename=input.split("\\")[len(input.split("\\"))-1]
    filename=os.path.split(input)[1]
    n=sendOnePkg(tcp, 100, sizeoffile, len(filename), struct.pack("%ds" % (len(filename)), filename))
    if 0 == n :
        trsLog("sendHeaderPkgError")
        fd.close()
        return 0
    for index in range(pkgnum):
        data=fd.read(BUFSIZ-DAT_HEAD_LEN)
        n=sendOnePkg(tcp, 200, index, BUFSIZ-DAT_HEAD_LEN, data)
        if 0 == n :
            trsLog("sendPkgError")
            fd.close()
            return 0
        if 0 == (index % 300) :
            view_bar(index,pkgnum)
    if not (0 == lastpkgsize) :
        data=fd.read(lastpkgsize)
        n=sendOnePkg(tcp, 200, pkgnum, lastpkgsize, data)
        if 0 == n :
            trsLog("sendPkgError")
            fd.close()
            return 0
    view_bar(pkgnum,pkgnum)
    fd.close()
    print ""
    trsLog('send \"%s\"[len:%d] successful\n\n' % (input, sizeoffile))
    return sizeoffile
def initClient(ADDR):
    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)
    return tcpCliSocket

def client(ADDR):
    #build socket 
    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)
    while True:
        input = raw_input('@@')
        trsLog("input is :%s\n" % input)
        trsLog("input.split()[0]:%s" % input.split()[0])
        if "s" == input :
            input = raw_input('pls drag file into windows:')
            #input="F:\\CALog\\pbn.isf"
            if not os.path.exists(input): 
                trsLog("\"%s\" is not exists!!!" % (input))
                continue
            sendOneFile(tcpCliSocket, input)
        elif "ls" == input :
            sendOnePkg(tcpCliSocket, 200, 0,0, "")
            print("\n%s\n"% (rcvInfo(tcpCliSocket)))
        elif "pwd" == input :
            sendOnePkg(tcpCliSocket, 201, 0,0, "")
            print("pwd:%s"% (rcvInfo(tcpCliSocket)))
        elif "cd" == input.split()[0] :
            sendOnePkg(tcpCliSocket, 202, 1,len(input), input)
            print("pwd:%s"% (rcvInfo(tcpCliSocket)))
        elif "get" == input.split()[0] :
            sendOnePkg(tcpCliSocket, 203, 1,len(input), input)
            data = tcpCliSocket.recv(BUFSIZ)
            if 0 == len(data) :
                trsLog("Receive Error")
                break
            (msgtype,index,datalen) = struct.unpack("3I",data[0:DAT_HEAD_LEN])
            info=""
            if 0 != datalen :
                (info,) = struct.unpack("%ds" % datalen,data[DAT_HEAD_LEN:(DAT_HEAD_LEN+datalen)])
            print "\n"
            trsLog("msgtype[%d], index[%d],datalen[%d] data:%s" % (msgtype,index,datalen,info))
            tcpCliSocket.send("ACK")
            if 100 == msgtype :
                time.sleep(1)
                filename=data[DAT_HEAD_LEN:DAT_HEAD_LEN+datalen]
                RecOneFile(tcpCliSocket, filename, index)
            else :
                trsLog("rcv error :msgtype=%d"%msgtype)
        elif "q" == input :
            sendOnePkg(tcpCliSocket, 300, 0,0, "")
            trsLog("quit")
            time.sleep(1)
            break
        else :
            trsLog("invalid cmd")
            continue

    tcpCliSocket.close()
tcpCliSocket = None
SendFlag = True
def SendPicThread() :
    global tcpCliSocket
    global SendFlag
    tcpCliSocket = initClient((str(sys.argv[2]),PORT))
    i = 0
    while SendFlag :
        i += 1
        sendOneFile(tcpCliSocket, os.path.join(".","%d.gif"%((i%7)+1)))
        time.sleep(0.1)
    
if __name__ == '__main__':
    global tcpCliSocket
    global SendFlag
    if 1 == len(sys.argv) :
        print("Pls Input Para -s , -c IP")
    elif "-s" == sys.argv[1] :
        trsLog("work in server")
        server(('',PORT))
    elif "-c" == sys.argv[1] :
        if 3 > len(sys.argv) :
            print("Pls Input Para -s , -c IP")
        else:
            trsLog("Work in client")
            t1=threading.Thread(target=SendPicThread)
            t1.setDaemon(True)
            t1.start()
            while True :
                inputCmd = raw_input(">>")
                if "q" == inputCmd :
                    SendFlag = False
                    time.sleep(1)
                    print "Quit Send Picture thread"
                    break
                else :
                    print "pls input q quit"
    else :
        print("Pls Input Para -s , -c IP")
    if None != tcpCliSocket : tcpCliSocket.close()





