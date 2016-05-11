# -*- coding: utf-8 -*-

import time
import logging
import logging.handlers
from collections import deque
import os

logQue = deque()
logger = logging.getLogger()
ALIVE = True

def alive(type):
    ALIVE = type



def Init(filepath, filename):
    fileMaxByte = 1024 * 1024 * 10  #10M
    if os.path.exists(filepath) is False:
	    os.mkdir(filepath)
    filePath = filepath + '/' + filename

    # logger = logging.getLogger()
    formatter =  logging.Formatter("%(asctime)s [%(module)s:%(lineno)d] %(message)s")
    fileHandler = logging.handlers.RotatingFileHandler(filePath, maxBytes=fileMaxByte, backupCount=10)
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    return logger



def setLevel( level ):
    if level == 'INFO':
        print("set INFO")
        logger.setLevel(logging.INFO)
    elif level == 'DEBUG':
        print("set DEBUG")
        logger.setLevel(logging.DEBUG)

def main(filename):
    # logger = logging.getLogger()
    logger = Init('log',filename)
    setLevel('INFO')
    while ALIVE:
        if len(logQue) <= 0:
            time.sleep(1)
        else:
            msg = logQue.popleft()
            logger.info(msg)


def PrintLog( msg ):
    logQue.append(msg)

if __name__ == '__main__':
    main('logger.log')
