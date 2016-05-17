# -*- coding: utf-8 -*-
import time
import threading
import socket
import writeLog
import recvSocket
import codecs

HOST = None
PORT = None

ALIVE = True




def alive(type):
    print("Socket Alive END")
    ALIVE = type


def readConfig( filePath ):
    data = ''
    with codecs.open(filePath, 'r', encoding='utf-8') as f:
        while True:
            tmp = f.readline()
            if tmp :
                data += tmp
            else :
                break

    return data



class sendSockThread(threading.Thread):
    def __init__(self, sendQue):
        threading.Thread.__init__(self)
        self.sendQue = sendQue
        self.alive = True
        self.host = ''
        self.port = 10001
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
            writeLog.PrintLog("make socket fail({})".format(ip))
            return -1

    def sendMsg(self, msg):
        if msg :
            # clientList =[]
            clientList = recvSocket.getClientList()
            # clientList.append('192.168.207.151')
            for client in clientList:
                try :
                    writeLog.PrintLog("client: {}".format(client))
                    sock = self.makeSocket(client)
                    if sock != -1 :
                        sock.send(msg.encode('utf-8'))
                        tmp = sock.recv(1024)
                        if tmp:
                            data = tmp.decode('utf-8').split('|')
                            if data[1] != 'OK':
                                writeLog.PrintLog("{}:{} is Incorrect{}".format(client, msg, data))
                            else:
                                writeLog.PrintLog("{}:{} is OK".format(client,data[1]))
                except:
                    writeLog.PrintLog("sendMsg {} is fail{}".format(client, msg))


    def run(self):
        writeLog.PrintLog("sendSockThr Start")
        try:
            while self.alive :
                if len(self.sendQue) <= 0:
                    time.sleep(0.5)
                    continue

                data = self.sendQue.popleft()
                if data:
                    tmp = data.split('|')
                    if tmp[0] == 'OPTION':
                        readData = readConfig(tmp[1])
                        data = tmp[0]+'|'+ readData

                    self.sendMsg(data)

                time.sleep(0.5)

        except :
            writeLog.PrintLog("sendSockThr Exception...")

        writeLog.PrintLog("sendSockThr End")

