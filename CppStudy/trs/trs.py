#!/bin/python
# -*- coding: utf-8 -*-

from socket import *
import time
import struct
import os
import sys
import commands

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
    
def RecOneFile(tcp, filename, filelen):
    trsLog("%s size is %d bytes" % (filename,filelen))
    pkgnum=filelen/(BUFSIZ-DAT_HEAD_LEN)
    lastpkgsize = filelen%(BUFSIZ-DAT_HEAD_LEN)
    trsLog("pkgnum is %d, lastpkgsize is %d" % (pkgnum, lastpkgsize))
    rcvFilepath=os.path.join(".","rcvFile")
    print("rcvFilepath is %s" % (rcvFilepath))
    if(not os.path.exists(rcvFilepath)) :
        os.makedirs(rcvFilepath)
    rcvFileName=os.path.join(rcvFilepath,filename)
    print("rcvFileName is %s" % (rcvFileName))
    if os.path.exists(rcvFileName) :
        rcvFileName = rcvFileName + "%f" % (time.time())
    print("rcvFileName2 is %s" % (rcvFileName))
    fd=open(rcvFileName,"ab")
    for index in range(pkgnum) :
        (msgtype,Rcvindex,rcvlen,rcvdata) = RevOneDataPack(tcp, index, BUFSIZ-DAT_HEAD_LEN)
        if 0 == rcvlen :
            fd.close()
            return 
        fd.write(rcvdata)
        if 0 == (index % 300) :
            view_bar(index, pkgnum)
        #trsLog("write file OK")
    if 0 != lastpkgsize :
        (msgtype,Rcvindex,rcvlen,rcvdata) = RevOneDataPack(tcp, pkgnum, lastpkgsize)
        if 0 == rcvlen :
            fd.close()
            return 
        fd.write(rcvdata)
        view_bar(pkgnum, pkgnum)
    print ""
    trsLog("write file OK")
    trsLog('Receive \"%s\"[len:%d] successful\n' % (filename, filelen))
    fd.close()

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
                time.sleep(1)
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

if __name__ == '__main__':
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
            client((str(sys.argv[2]),PORT))
    else :
        print("Pls Input Para -s , -c IP")






