# -*- coding: utf-8 -*-
import os
import time
import log
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


clientList = []


def gAlive(type):
    g_alive = type



def cmd_msg():
    platform_os = platform.system()
    if platform_os == 'win':
        os.system("cls")
    else:
        os.system("clear")

    print("============== WK ProxyServer Performance cmd ==============")
    print("======= cmd.txt file is select ( which line is cmd ) =======")
    line= input("> ")
    if line :
        if int(line) >0 :
            with codecs.open('cmd.txt', 'r', encoding='utf=8') as f:
                for idx in range(int(line)):
                    cmd = f.readline()

    return cmd.strip()

def main():

    recvQue = deque()
    sendQue = deque()

    logThr =  log.logThread('log', 'logger.log')
    recvSockThr = recvSocket.recvSockThread(recvQue)
    sendSockThr = sendSocket.sendSockThread(sendQue)

    logThr.start()
    sendSockThr.start()
    recvSockThr.start()

    log.PrintLog("PerformanceServer start")
    time.sleep(1)
    while g_alive:
        try:
            data = cmd_msg()
            print("select cmd: {}".format(data))
        except Exception as e:
            log.PrintLog("[main] except :{}".format(sys.exc_info()[0]))
        time.sleep(1)

    log.PrintLog("PerformanceServer end")

if __name__ == "__main__":
    main()
