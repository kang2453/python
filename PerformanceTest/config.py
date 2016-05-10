# -*- coding: utf-8 -*-

import codecs

# option담을 DIC
Option = {}

#각각 옵션 DIC
cmddic   = {}
proxydic  = {}
sitedic   = {}

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
    with codecs.open(filename, 'r', encoding='utf-8') as f:
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



def main():
    pass



if __name__ == '__main__':
    main()
