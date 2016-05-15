# -*- coding: utf-8 -*-
import time
import threading
import socket
import log

HOST = None
PORT = None

ALIVE = True

global clientList


def alive(type):
    print("Socket Alive END")
    ALIVE = type


class sendSockThread(threading.Thread):
    def __init__(self, sendQue):
        threading.Thread.__init__(self)
        self.sendQue = sendQue
        self.alive = True
        self.host = ''
        self.port = 10001
        self.log = log.logger
        self.sock = -1

    def isAlive(self):
        return self.alive


    def setAlive(self, type ):
        self.alive = type


    def makeSocket(self, ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ADDR = (ip, 10001)
            sock.connect(ADDR)
            return sock
        except:
            log.PrintLog("make socket fail({})".format(ip))
            return -1

    def sendMsg(self, msg):

        if msg :
            for client in clientList:
                try :
                    sock = self.makeSocket(client)
                    if sock != -1 :
                        sock.send(msg.encode('utf-8'))
                        data = sock.recv(1024)
                        if data:
                            tmp = data.split('|')
                            if tmp[1] != 'OK':
                                log.PrintLog("{}:{} is Incorrect{}".format(client, msg, data))

                except:
                    log.PrintLog("sendMsg {} is fail{}".format(client, msg))




    def run(self):
        log.PrintLog("sendSockThr Start")
        try:
            while self.alive :
                if len(self.sendQue) <= 0:
                    time.sleep(0.5)
                    continue

                data = self.sendQue.popleft()
                if data:
                    self.sendMsg(data)

                time.sleep(0.5)

        except :
            log.PrintLog("sendSockThr Exception...")

        log.PrintLog("sendSockThr End")

