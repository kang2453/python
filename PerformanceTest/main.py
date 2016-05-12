# -*- coding: utf-8 -*-
import codecs
import threading
import time
import log
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


configFileName = 'config.conf'

def gAlive(type):
    g_alive = type

def main():
    recvQue = deque()
    msgQue = deque()
    sendQue = deque()

    # logThr = threading.Thread(target=log.main, args=('logger.log', ))
    # msgHandleThr = threading.Thread(target=msgHandle.main, args=(Option, recvQue, msgQue))
    # siteThr = threading.Thread(target=sitelist.main, args=(Option, msgQue, sendQue))

    # sendSockThr = threading.Thread(target=sendSocket.main, args=(Option, sendQue))
    # recvSockThr = threading.Thread(target=recvSocket.main, args=(Option, recvQue))

    logThr =  log.logThread( 'log', 'logger.log')
    sitelistThr = sitelist.sitelistThread( Option, msgQue, sendQue )
    msgHandlerThr = msgHandle.msgHandleThread(recvQue, msgQue)
    recvSockThr = recvSocket.recvSockThread(Option, recvQue)

    logThr.start()
    sitelistThr.start()
    msgHandlerThr.start()
    recvSockThr.start()


    cnt = 0
    while g_alive:
        if cnt == 100:
            gAlive(False)
            sitelist.alive(False)
            recvSockThr.setAlive(False)
            sendSocket.alive(False)
            msgHandle.alive(False)
            log.alive(False)
            break
        cnt += 1
        time.sleep(1)
    log.PrintLog("MAIN END")

if __name__ == "__main__":
    Option = config.getOption('config.conf')
    main()
