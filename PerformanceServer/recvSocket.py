# -*- coding: utf-8 -*-

import threading
import time
import log
import socket
import sys

BUFSIZE = 1024

def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    return s.getsockname()[0]


class recvSockThread( threading.Thread ):
    def __init__(self, recvQue):
        threading.Thread.__init__(self)
        self.recvQue = recvQue
        self.alive   = True
        self.host    = ''
        self.port    = 10011
        self.log     = log.logger
        self.sock = -1

    def isAlive(self):
        return self.alive

    def setAlive(self, type):
        self.alive = type

    def makeSocket(self):
        retVal = True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.host = myip()
            # self.host = 'localhost'
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
                        log.PrintLog("%s is Connected(%s)" % (str(addrInfo), data))
                        if data:
                            cmd = data.decode('utf-8')
                            data = cmd.split('|')
                            self.recvQue.append(data)
                            msg = data[0] + "|OK"
                            cliSock.send(msg.encode('utf-8'))
                        else:
                            time.sleep(0.5)
                        cliSock.close()
                    except socket.error as e:
                        log.PrintLog("recvSocket client Exception({})".format(e))
                    except :
                        log.PrintLog("recvSocket client Exception...")
                self.sock.close()
        except:
            log.PrintLog("RecvSocket Exception....")
        log.PrintLog("recvSockThr END")



