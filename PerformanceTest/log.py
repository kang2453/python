# -*- coding: utf-8 -*-

import time
import logging
import logging.handlers
import threading
from collections import deque

import os

logQue = deque()
logger = logging.getLogger()
ALIVE = True


class logThread(threading.Thread):
    def __init__(self, filepath, filename):
        threading.Thread.__init__(self)
        self.filepath = filepath
        self.filename = filename
        self.alive    = True
        self.sep      = os.sep
        self.level    = 'WARNING'
        self.filesize = 1024*1024*5 #5M

    def isAlive(self):
        return self.alive

    def setAlive(self, type ):
        self.alive = type

    def Init(self):
        if os.path.exists(self.filepath) is False:
            os.mkdir(self.filepath)
        logfilePath = self.filepath + self.sep + self.filename

        formatter =  logging.Formatter("%(asctime)s %(message)s","%Y-%m-%d %H:%M:%S")
        fileHandler = logging.handlers.RotatingFileHandler(logfilePath, maxBytes=self.filesize, backupCount=10)
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)
        return logger

    def setLevel( self, level ):
        if level == 'INFO':
            self.level = logging.INFO
            logger.setLevel(logging.INFO)
        elif level == 'DEBUG':
            self.level = logging.DEBUG
            logger.setLevel(logging.DEBUG)

    def run(self):
        PrintLog("logThread START")
        logger = self.Init()
        self.setLevel(self.level)
        while self.alive:
            if len(logQue) <= 0:
                time.sleep(0.5)
            else:
                msg = logQue.popleft()
                logger.info(msg)
        PrintLog("logThread END")

def PrintLog( msg ):
    logQue.append(msg)
