# -*- coding: utf-8 -*-

import logging
import logging.handlers


def Init(filepath, filename):
    fileMaxByte = 1024 * 1024 * 10  #10M
    filePath = filepath + '/' + filename

    logger = logging.getLogger()
    formatter =  logging.Formatter("%(asctime)s [%(module)s:%(lineno)d] %(message)s")
    fileHandler = logging.handlers.RotatingFileHandler(filePath, maxBytes=fileMaxByte, backupCount=10)
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    return logger


def setLevel( level, logger ):
    if level == 'INFO':
        print("set INFO")
        logger.setLevel(logging.INFO)
    elif level == 'DEBUG':
        print("set DEBUG")
        logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    main()
