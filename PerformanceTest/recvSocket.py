# -*- coding: utf-8 -*-

import threading
import time
import log
from socket import *
import sys

BUFSIZE = 1024

class recvSockThread( threading.Thread ):
    def __init__(self, option, recvQue):
        threading.Thread.__init__(self)
        self.option = option
        self.recvQue = recvQue
        self.alive   = True
        self.cmdDic  = self.option['cmd']
        self.host    = ''
        self.port    = 10001
        self.log     = log.logger
        self.sock = socket(AF_INET, SOCK_STREAM)

    def isAlive(self):
        return self.alive

    def setAlive(self, type):
        self.alive = type

    def makeSocket(self):
        try:
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            HOST = self.sock.gethostbyname(self.sock.gethostname())
            print("host : ", self.host)
            ADDR = (self.host, self.port )
            self.sock.bind(ADDR)
            self.sock.listen(5)
        except socket.error as msg :
            log.PrintLog("makeSocket is Fail(%s)"% (msg))

    def InsertQue(self, data):
        self.recvQue.append(data)


    def run(self):
        log.PrintLog("recvSockThr START")
        try:
            # makeSocket()
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            # HOST = self.sock.gethostbyname(self.sock.gethostname())
            # print("host : ", self.host)
            ADDR = (self.host, self.port )
            self.sock.bind(ADDR)
            self.sock.listen(5)
            while self.alive :
                cliSock, addrInfo = self.sock.accept()
                log.PrintLog("%s is Connected" % str(addrInfo))
                data = cliSock.recv(BUFSIZE)
                if data:
                    log.PrintLog("Recv Msg: %s" % data )
                    cmd = data.split('|')
                    msg = cmd + "|OK"
                    cliSock.send(msg)
                    cliSock.close()
                else:
                    self.cliSock.close()
                    log.PrintLog("%s is disconnected" % str(addrInfo))
            self.sock.close()
        except:
            log.PrintLog("RecvSocket Exception....")
        log.PrintLog("recvSockThr END")



