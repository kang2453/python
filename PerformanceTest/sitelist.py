# -*- coding: utf-8 -*-

import time

from Main import getOption

HOST    = '192.168.207.50'
PORT    = 8080
THREADNUM = 10
CNT     = 1000

TYPE    = 'http'
VERSION = 9
REQTYPE = "LM"
LDATE   =   "20160401000000"



ALIVE = True
siteDic = {}


# httpGetFileListUrl  = 'http://192.168.207.50:8080/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpsGetFileListUrl = 'https://192.168.207.50:8443/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpGetFileUrl      = 'http://192.168.207.50:8080/70WKDownloader/getFile.aspx?id=webkeeper&pwd=vhvrn755&version=8&filename=SiteList6.db3&uid=filyp123&rcvname=test'

GetFileListUrl ='70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
GetFileUrl     = '70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='







def alive(type):
    ALIVE = type



def httpGetFileList(cnt):
    i = 0
    try:
       while i < cnt:
           for http in TYPE:
                print("httpGetFileList", i)
                i += 1
    except:
        print("Exception... httpGetFileList" )


def httpTest(cnt):
    print("http TEST CNT: ", cnt)
    httpGetFileList(cnt)



def print_option():
    print("========= SiteList ======")
    print("Type     : ", TYPE)
    print("ThreadNum: ", THREADNUM )
    print("Cnt      : ", CNT)
    print("VERSION  : ", VERSION)
    print("REQTYPE  : ", REQTYPE)
    print("LDATE    : ", LDATE)
    print("========= ProxyServer ======")
    print("HOST     : ", HOST )
    print("PORT     : ", PORT )

def getOption(option):
    print(option)
    siteDic = option['sitelist']
    TYPE    = siteDic['TYPE']
    REQTYPE = siteDic['REQTYPE']
    LDATE   = siteDic['LDATE']
    VERSION = siteDic['VERSION']
    THREADNUM=siteDic['THREADNUM']
    CNT     = siteDic['CNT']

    cmdDic = option['proxy']
    HOST = cmdDic['PROXYSERVER']
    PORT = cmdDic['PROXYPORT']
    
    return True

def main(option, Que):
    rv = getOption(option)
    if rv is False:
        #print("SiteList Thr option parsing Error")
        alive(False)
        SystemExit(0)

    print_option()

    httpTest(int(CNT)) 
    time.sleep(1)

    #print("SiteList Thread END!!!")


if __name__ == "__main__":
    main(option,Que )
