# -*- coding: utf-8 -*-

import threading
import time
import writeLog
import socket
import sys
from collections import deque

BUFSIZE = 1024


clientList = []



def myip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    return s.getsockname()[0]

def InsertClient( clientip ):
    isSame = False
    for ip in clientList:
        if ip == clientip:
            isSame = True
            break

    if isSame is False:
        clientList.append(clientip)


def getClientList():
    return clientList


class recvSockThread( threading.Thread ):
    def __init__(self, recvQue):
        threading.Thread.__init__(self)
        self.recvQue = recvQue
        self.alive   = True
        self.host    = ''
        self.port    = 10011
        self.log     = writeLog
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
            writeLog.PrintLog("makeSocket is Fail(%s)"% (msg))
            retVal = False
        return retVal

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
                        writeLog.PrintLog("%s is Connected(%s)" % (str(addrInfo[0]), data))
                        if data:
                            cmd = data.decode('utf-8')
                            data = cmd.split('|')
                            msg = data[0] + "|OK"
                            cliSock.send(msg.encode('utf-8'))
                            InsertClient(data[1])
                        else:
                            time.sleep(0.5)
                        cliSock.close()
                    except socket.error as e:
                        writeLog.PrintLog("recvSocket client Exception({})".format(e))
                    except :
                        writeLog.PrintLog("recvSocket client Exception...")
                self.sock.close()
        except:
            writeLog.PrintLog("RecvSocket Exception....")
        writeLog.PrintLog("recvSockThr END")



