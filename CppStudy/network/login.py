#!/usr/bin/env python
import httplib, urllib
import socket
import sys, os
from urlparse import urlparse
from getpass import getpass
httplib.HTTPConnection.debuglevel = 0
marker = "http://www.baidu.com"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

'''
%25%25MAGICID%25%25=%25%25MAGICVAL%25%25&lang=chs&username=${account}&encryptToken=&passwd=********&pwd=${password}
'''

def encrypt(passwd):
    m=7777817
    e=91 
    epasswd=''
    for c in passwd:
        epasswd+="%.8x" % pow(ord(c),e,m)
    return epasswd

def lookup_proxy_auth_ip(proxy):
    conn = httplib.HTTPConnection(proxy)
    conn.request("GET", marker + "/")
    response = conn.getresponse()
    conn.close()
    if response.status == httplib.FOUND:
        for item in response.getheaders(): 
          if item[0]=='location':
              return response.status, item[1]
    return response.status, None


proxy = os.getenv("http_proxy") or \
        os.getenv("HTTP_PROXY") or \
        raw_input("Proxy sever: ")
proxy = urlparse(proxy).netloc or proxy

#account=raw_input("User account: ")
account="10117906"

#passwd=getpass()
passwd='zkm0.12345'
status, proxy = lookup_proxy_auth_ip(proxy)
if status == httplib.OK:
    print bcolors.OKGREEN + "You already can access %s" % marker+bcolors.ENDC
    sys.exit(0)
#print("proxy is %s, passwd is %s" % (proxy,passwd))
proxy = urlparse(proxy).netloc
passwd = encrypt(passwd)
#print("proxy is %s, passwd is %s" % (proxy,passwd))

params = urllib.urlencode({'%%MAGICID%%': "%%MAGICVAL%%", 'lang': 'en',
    'username': account, 'encryptToken': '',
    'passwd': '********',
    'pwd': passwd})
#print(params)
headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}
conn = httplib.HTTPConnection(proxy)
#print(conn)
conn.request("POST", "/", params, headers)
response = conn.getresponse()
conn.close()
if response.status == httplib.OK:
    print bcolors.OKGREEN+"Login Success. Enjoy your surf! (^.^)"+bcolors.ENDC
