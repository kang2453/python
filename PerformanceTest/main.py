# -*- coding: utf-8 -*-
import time
import writeLog
import sys
import socket
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

    logThr =  writeLog.logThread( 'log', 'logger.log')
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

    writeLog.PrintLog("Performance Test Start")
    print("Performance Test Start")
    while g_alive:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(ADDR)
            sock.send(msg.encode('utf-8'))
            data = sock.recv(BUFSIZE)
            writeLog.PrintLog("{} -> {}".format(cmdDic['IP'], data.decode('utf-8')))
            sock.close()
            time.sleep(10)
        except socket.error as e:
            writeLog.PrintLog("[main] exception({} - {})".format(e, msg))
        except Exception as e:
            writeLog.PrintLog("[main] except :{}".format(sys.exc_info()[0]))
        time.sleep(10)
    writeLog.PrintLog("Performance Test End")
    print("Performance Test End")

if __name__ == "__main__":
    Option = config.getOption('config.conf')
    main()
