# -*- coding: utf-8 -*-

import time
import threading
import codecs
from collections import deque

import os
import sys
import platform
logQue = deque()

def isWindows():
    if platform.system() == 'Windows':
        return True
    else:
        return False

class logThread(threading.Thread):
    def __init__(self, filepath, filename):
        threading.Thread.__init__(self)
        self.filepath = filepath
        self.filename = filename
        self.alive    = True
        self.sep      = os.sep
        self.filesize = 1024*1024*5 #5M
        self.fd       = -1
        self.linesep  = ""

    def isAlive(self):
        return self.alive

    def setAlive(self, type ):
        self.alive = type

    def initFile(self):
        if os.path.exists(self.filepath) is False:
            os.mkdir(self.filepath)

        logfilePath = self.filepath + self.sep + self.filename

        if isWindows() is True:
            self.linesep = '\r\n'
        else:
            self.linesep = '\n'

        logfilePath = self.filepath + self.sep + self.filename
        self.fd = codecs.open(logfilePath, 'a', encoding='utf-8')

    def Write(self, msg):
        timestr = time.strftime("%Y-%m-%d %H:%M:%S")
        data = "{} {}{}".format(timestr, msg, self.linesep)
        self.fd.write(data)
        self.fd.flush()

    def Writelog(self, msg):
        try:
            # print(msg)
            self.Write(msg)
        except IOError as e :
            self.fd.close()
            self.initFile()
            self.Write(msg)

    def run(self):
        self.initFile()
        PrintLog("logThread Start")
        while self.alive:
            if len(logQue) <= 0:
                time.sleep(0.5)
            else:
                msg = logQue.popleft()
                self.Writelog(msg)

        self.fd.close()



def PrintLog( msg ):
    logQue.append(msg)