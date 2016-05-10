# -*- coding: utf-8 -*-

import time
import log



ALIVE = True
siteDic = {}
cmdDic  = {}
proxyDic = {}

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
           for http in siteDic['TYPE']:
                # print("httpGetFileList", i)
                msg = 'httpGetFileList' + str(i)
                log.PrintLog(msg)
                i += 1
    except:
        print("Exception... httpGetFileList" )


def httpTest(cnt):
    print("http TEST CNT: ", cnt)
    httpGetFileList(cnt)



def print_option():
    print("========= SiteList ======")
    print("Type     : ", siteDic['TYPE'])
    print("ThreadNum: ", siteDic['THREADNUM'] )
    print("Cnt      : ", siteDic['CNT'])
    print("VERSION  : ", siteDic['VERSION'])
    print("REQTYPE  : ", siteDic['REQTYPE'])
    print("LDATE    : ", siteDic['LDATE'])
    print("========= ProxyServer ======")
    print("HOST     : ", proxyDic['PROXYSERVER'] )
    print("PORT     : ", proxyDic['PROXYPORT'] )

def getOption(option):
    print(option)
    global siteDic
    global cmdDic
    global proxyDic

    siteDic = option['sitelist']
    proxyDic= option['proxy']
    return True

def main(option, msgQue, sendQue):
    rv = getOption(option)
    if rv is False:
        #print("SiteList Thr option parsing Error")
        alive(False)
        SystemExit(0)

    # print_option()
    print('cnt : ', siteDic['CNT'])
    httpTest(int(siteDic['CNT']))
    time.sleep(1)

    #print("SiteList Thread END!!!")


if __name__ == "__main__":
    main(option, msgQue, sendQue )
