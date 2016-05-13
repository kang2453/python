# -*- coding: utf-8 -*-

import codecs
import os
import log
import sys


# option담을 DIC
Option = {}

#각각 옵션 DIC
cmddic   = {}
proxydic  = {}
sitedic   = {}

configDir  = "conf"
configFile = "config.conf"


def ParsingOption(type, msg):
    tmp = msg.split('=')
    if len(tmp) == 2:
        if type =='cmd':
            cmddic[tmp[0]] = tmp[1]
        elif type == 'proxy':
            proxydic[tmp[0]] = tmp[1]
        elif type == 'sitelist':
            sitedic[tmp[0]] = tmp[1]

def getOption(filename):
    configFile = filename
    if os.path.exists(configDir) is False:
        os.mkdir(configDir)

    filePath = configDir + os.sep + filename
    with codecs.open(filePath, 'r', encoding='utf-8') as f:
        type = ""
        while True:
            msg = f.readline().strip()
            if not msg:
                break
            if msg[0] == '#':
                continue
            if msg.find("[CMD]") != -1:
                type = 'cmd'
                continue
            elif msg.find("[PROXY]") != -1:
                type = 'proxy'
                continue
            elif msg.find("[SITELIST]") != -1:
                type = 'sitelist'
                continue

            ParsingOption(type, msg)
        Option['cmd'] = cmddic
        Option['proxy'] = proxydic
        Option['sitelist'] = sitedic
    return Option


def update( value ):
    filePath = configDir + os.sep + configFile
    try:
        with codecs.open(filePath, 'w', encoding='utf-8') as f:
            f.write(value)
    except :
        log.PrintLog("conf Update Except....")

def confDic( f, dic ):
    pass

def configWrite():
    filePath = configDir + os.sep + configFile
    with codecs.open(filePath, 'a', encoding='utf-8') as f:
        f.writeline('#Config Setting')
        f.writeline('[CMD]')
        confDic(f, cmddic)
        f.writeline('[PROXY]')
        confDic(f, proxydic)
        f.writeline('[SITELIST]')
        confDic(f, sitedic)




