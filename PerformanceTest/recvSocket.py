# -*- coding: utf-8 -*-

import threading
import time
import writeLog
import socket
import sys

BUFSIZE = 1024

def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    return s.getsockname()[0]


class recvSockThread( threading.Thread ):
    def __init__(self, option, recvQue):
        threading.Thread.__init__(self)
        self.option = option
        self.recvQue = recvQue
        self.alive   = True
        self.cmdDic  = self.option['cmd']
        self.host    = ''
        self.port    = 10001
        self.log     = writeLog
        self.sock = -1

    def isAlive(self):
        return self.alive

    def setAlive(self, type):
        self.alive = type

    def makeSocket(self):
        retval = True
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.host = myip()
            ADDR = (self.host, self.port)
            self.sock.bind(ADDR)
            self.sock.listen(5)
        except socket.error as msg :
            writeLog.PrintLog("makeSocket is Fail(%s)"% (msg))
            retval = False
        return retval

    def run(self):
        writeLog.PrintLog("recvSockThr START")
        try:
            retVal = True
            retVal = self.makeSocket()
            if retVal is True:
                while self.alive :
                    try:
                        cliSock, addrInfo = self.sock.accept()
                        data = cliSock.recv(BUFSIZE)
                        writeLog.PrintLog("%s is Connected(%s)" % (str(addrInfo), data))
                        if data:
                            cmd = data.split('|')
                            self.recvQue.append(data.decode('utf-8'))
                            msg = cmd[0] + "|OK"
                            cliSock.send(msg.encode('utf-8'))
                        else:
                            time.sleep(0.5)
                        cliSock.close()
                    except socket.error as e:
                        writeLog.PrintLog("recvSocket client Exception...({})".format(e))
                self.sock.close()
        except:
            writeLog.PrintLog("RecvSocket Exception....")
        writeLog.PrintLog("recvSockThr END")



