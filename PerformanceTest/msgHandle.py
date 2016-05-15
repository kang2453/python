# -*- coding: utf-8 -*-
import time
import threading
import log
import config
from collections import deque


class  msgHandleThread( threading.Thread ):
    def __init__(self, recvQue, msgQue):
        threading.Thread.__init__(self)
        self.recvQue = recvQue
        self.msgQue  = msgQue
        self.alive   = True
        self.log     = log.logger

    def isAlive(self):
        return self.alive

    def setAlive(self, type ):
        self.alive = type


    def msgHandle(self, cmd, value):
        if cmd == 'OPTION':
            # 옵션은 여기에서 변경하고
            # sitelist.py에서는 다시 읽으라고 한다.
            # value로 받은거 그대로 저장함
            config.update(value)
            self.msgQue.append('RELOAD!config.conf')
        # 명령 수행 MSG
        elif cmd == 'CMD':
            # sitelist 성능 측정관련 메시지
            self.msgQue.append(value)
        # 업데이트 관련 MSG
        elif cmd == 'UPDATE':
            self.msgQue.append(value)
        else:
            log.PrintLog("%s:%s msg is not define" % (cmd, value))




    def run(self):
        log.PrintLog("msgHandler START")
        while self.alive:
            if len(self.recvQue) > 0:
                data = self.recvQue.popleft()
                log.PrintLog("recvQue: {}".format(data))
                msg  = data.split('|')
                self.msgHandle(msg[0], msg[1])
            else:
                time.sleep(0.5)

        log.PrintLog("msgHandler is Exit")


