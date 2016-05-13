# -*- coding: utf-8 -*-
import codecs
import threading
import time
import log
import re
import urllib
import  socket
from collections import deque

import recvSocket
import sendSocket
import sitelist
import msgHandle

import config

# option담을 DIC
Option = None

# thread 객체 담을곳
threads = []
g_alive = True
BUFSIZE=1024

configFileName = 'config.conf'

def gAlive(type):
    g_alive = type

def main():
    recvQue = deque()
    msgQue = deque()
    sendQue = deque()

    logThr =  log.logThread( 'log', 'logger.log')
    sitelistThr = sitelist.sitelistThread( Option, msgQue, sendQue )
    msgHandlerThr = msgHandle.msgHandleThread(recvQue, msgQue)
    recvSockThr = recvSocket.recvSockThread(Option, recvQue)

    logThr.start()
    sitelistThr.start()
    msgHandlerThr.start()
    recvSockThr.start()

    cmdDic = Option['cmd']

    myip=  recvSocket.myip()
    ADDR=(cmdDic['IP'], 10011)
    msg =  "CONNECT|{}".format(myip)
    # log.PrintLog(msg)

    while g_alive:
        try:
            sock = socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(ADDR)
            sock.send(msg.encode('utf-8'))
            data = sock.recv(BUFSIZE)
            log.PrintLog("%s -> %s".format(msg, data.decode('utf-8')))
            sock.close()
            time.sleep(10)
        except socket.timeout:
            pass
        except socket.error as errMsg:
            log.PrintLog(errMsg.string)
        time.sleep(10)
    log.PrintLog("MAIN END")

if __name__ == "__main__":
    Option = config.getOption('config.conf')
    main()
