# -*- coding: utf-8 -*-

import time
import log
import threading


isStop  = False
siteDic = {}
cmdDic  = {}
proxyDic = {}

# httpGetFileListUrl  = 'http://192.168.207.50:8080/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpsGetFileListUrl = 'https://192.168.207.50:8443/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpGetFileUrl      = 'http://192.168.207.50:8080/70WKDownloader/getFile.aspx?id=webkeeper&pwd=vhvrn755&version=8&filename=SiteList6.db3&uid=filyp123&rcvname=test'

GetFileListUrl ='70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
GetFileUrl     = '70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='


threadList = []

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


class sitelistThread(threading.Thread):
    def __init__(self, option, msgQue, sendQue):
        threading.Thread.__init__(self)
        self.msgQue = msgQue
        self.sendQue = sendQue
        self.alive   = True
        self.option  = option
        self.log     = log.logger


    def isAlive(self):
        return self.alive

    def setAlive(self, type ):
        self.alive = type

    def httpTest(self, cnt):
        thrCnt = siteDic['THREADNUM']
        if thrCnt <= 0:
            thrCnt = 1

        for i in thrCnt:
            name = "thread-{}".format(i)
            t =   threading.Thread(target=httpGetFileList, args=(name, cnt))
            t.name = "thread-{}".format(i)
            threadList.append(t)

        startTime = time.time()
        for id in threadList:
            id.start()

        for id in threadList:
            id.join()

        endTime = time.time()
        return endTime - startTime


    def print_option(self):
        print("========= SiteList ======")
        print("Type     : ", siteDic['TYPE'])
        print("ThreadNum: ", siteDic['THREADNUM'] )
        print("VERSION  : ", siteDic['VERSION'])
        print("REQTYPE  : ", siteDic['REQTYPE'])
        print("LDATE    : ", siteDic['LDATE'])
        print("========= ProxyServer ======")
        print("HOST     : ", proxyDic['PROXYSERVER'] )
        print("PORT     : ", proxyDic['PROXYPORT'] )

    def getOption(self):
        global siteDic
        global cmdDic
        global proxyDic

        # print(self.option)
        siteDic = self.option['sitelist']
        proxyDic= self.option['proxy']
        log.PrintLog(siteDic)
        log.PrintLog(proxyDic)
        return True

    def msgHandler(self, msg):
        data = msg.split('=')
        if data[0] == 'CMD':
            cmdDic = data[1]
        elif data[0] == 'PROXY':
            proxyDic = data[1]
        elif data[0] == 'SITELIST':
            siteDic = data[1]
        elif data[0] == 'START':
            retVal = None
            retVal = self.httpTest(int(data[1]))
            if retVal is None:
                logStr = "httpTest is InCorrect"
                log.PrintLog(logStr)
            else:
                self.sendQue.append(retVal)
        elif data[0] == 'STOP':
            isStop = True
        elif data[0] == 'DELETE':
            self.deleteFiles()
        else:
            log.PrintLog("%s msg is not Define".format(msg))




    def run(self):
        log.PrintLog("SiteListThread START")
        retVal = self.getOption()
        if retVal is False:
            log.PrintLog("sitelistThr option Parsing is Fial(", self.option, ")")
            self.setAlive(False)

        while self.alive:
            if len(self.msgQue) <= 0 :
                time.sleep(0.5)
                continue

            data = self.msgQue.popleft()
            if data:
                self.msgHandler(data)

        log.PrintLog("SiteListThread END")





