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
        self.host    = '192.168.207.50'
        self.port    = 10001
        self.log     = log.logger
        self.sock = socket(AF_INET, SOCK_STREAM)

    def isAlive(self):
        return self.alive

    def setAlive(self, type):
        self.alive = type

    def makeSocket(self):
        retVal = True
        try:
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            ADDR = (self.host, self.port)
            self.sock.bind(ADDR)
            self.sock.listen(5)
        except socket.error as msg :
            log.PrintLog("makeSocket is Fail(%s)"% (msg))
            retVal = False
        return retVal

    def run(self):
        log.PrintLog("recvSockThr START")
        try:
            retVal = True
            retVal = self.makeSocket()
            if retVal is True:
                while self.alive :
                    try:
                        cliSock, addrInfo = self.sock.accept()
                        data = cliSock.recv(BUFSIZE)
                        log.PrintLog("%s is Connected(%s)" % (str(addrInfo),data))
                        if data:
                            cmd = data.split('|')
                            if len(cmd) == 2:
                                msg = cmd[0] + "|OK"
                                cliSock.send(msg.encode('utf-8'))
                                self.recvQue.append(data.decode('utf-8'))
                        cliSock.close()
                    except :
                        log.PrintLog("%s msg is incorrect: %s" % (msg, str(addrInfo[0])))
                self.sock.close()
        except:
            log.PrintLog("RecvSocket Exception....")
        log.PrintLog("recvSockThr END")



