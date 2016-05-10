# -*- coding: utf-8 -*-

import time
import log

HOST = None
PORT = None

ALIVE = True

dic = {}

def alive(type):
    print("Socket Alive END")
    ALIVE = type

def getOption(option):
    dic= option['cmd']
    log.PrintLog(dic)



def main(option, recvQue):
    rv = getOption(option)
    if rv is False:
        log.PrintLog("get option fail")
    cnt = 0
    while ALIVE:
        #print("socket main ", cnt)
        cnt += 1
        if cnt == 10 :
            break
        time.sleep(1)
    log.PrintLog("recvSockThr END")

if __name__ == "__main__":
    main(option, recvQue)
