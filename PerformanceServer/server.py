# -*- coding: utf-8 -*-

import os
import time
import writeLog
import sys
import platform
from collections import deque

import recvSocket
import sendSocket
import codecs

# thread 객체 담을곳
threads = []
g_alive = True
BUFSIZE=1024

configFileName = 'config.conf'

# clientList = []

def gAlive(type):
    g_alive = type

def isWindows():
    if platform.system() == 'Windows':
        return True
    else:
        return False

def ReadCmd():
    lineNum = 1
    with codecs.open('cmd.txt', 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            line = line.strip()
            if line :
                print("%d -- %s" % (lineNum, line.strip()))
                lineNum += 1
            else:
                break


def cmd_msg():
    if isWindows() is True:
        os.system("cls")
    else:
        os.system("clear")

    print("============== WK ProxyServer Performance cmd ==============")
    ReadCmd()
    print("======================= ReFresh : R ========================")
    print("======= cmd.txt file is select ( which line is cmd ) =======")
    line= input("> ")
    if line :
        if line == 'R':
            return ''
        if int(line) >0 :
            with codecs.open('cmd.txt', 'r', encoding='utf=8') as f:
                for idx in range(int(line)):
                    cmd = f.readline()

    return cmd.strip()

def main():

    recvQue = deque()
    sendQue = deque()

    logThr =  writeLog.logThread('log', 'logger.log')
    recvSockThr = recvSocket.recvSockThread(recvQue)
    sendSockThr = sendSocket.sendSockThread(sendQue)

    logThr.start()
    sendSockThr.start()
    recvSockThr.start()

    writeLog.PrintLog("PerformanceServer start")
    time.sleep(1)
    while g_alive:
        try:
            data = cmd_msg()
            print("select cmd: {}".format(data))
            if data:
                sendQue.append(data)

            time.sleep(1)
        except Exception as e:
            writeLog.PrintLog("[main] except :{}".format(e.msg))
        time.sleep(1)

    writeLog.PrintLog("PerformanceServer end")

if __name__ == "__main__":
    # printnull()
    main()
