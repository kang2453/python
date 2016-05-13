# -*- coding: utf-8 -*-

import os
import time
import log
import threading
import requests
import shutil
import config
import sys

isStop  = False
siteDic = {}
cmdDic  = {}
proxyDic = {}

param = {}


cafile='server.wk.somansa.pem'
keyfile='server.wk.somansa.key'
passphrase='pass1234'

# httpGetFileListUrl  = 'http://192.168.207.50:8080/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpsGetFileListUrl = 'https://192.168.207.50:8443/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpGetFileUrl      = 'http://192.168.207.50:8080/70WKDownloader/getFile.aspx?id=webkeeper&pwd=vhvrn755&version=8&filename=SiteList6.db3&uid=filyp123&rcvname=test'
GetFileListUrl ='/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=$VERSION&reqtype=$REQTYPE&uid=fpwlkb0&rcvname=wkAgent&ldate=$LDATE&SN='
GetFileUrl     = '/70WKDownloader/getFile.aspx?id=webkeeper&pwd=vhvrn755&version=$VERSION&filename=$FILENAME&uid=fpwlkb0&rcvname=wkAgent&SN='

threadList = []

def getExt(reqtype):
    if reqtype.find('L') == -1:
        ext = ".mdb"
    else:
        ext = ".db3"
    return ext



def getFileListUrl(isHttp ):

    server = proxyDic['PROXYSERVER']
    idx = proxyDic['PROXYPORT'].find(',')
    if idx == -1:
        httpPort = '8080'
        httpsPort = '8443'
    else:
        tmps = proxyDic['PROXYPORT'].split(',')
        for data in tmps:
            if data.find('HTTPS') != -1:
                httpsPort = data.split(':')[1]
            elif data.find('HTTP') != -1:
                httpPort = data.split(':')[1]
            else:
                log.PrintLog("Option PROXYPORT is Incorrect(default: 8080, 8443")
                httpPort = "8080"
                httpsPort = "8443"

    filelisturl = GetFileListUrl
    filelisturl = filelisturl.replace('$VERSION',  param['VERSION'])
    filelisturl = filelisturl.replace('$REQTYPE',  param['REQTYPE'])
    filelisturl = filelisturl.replace('$LDATE', param['LDATE'])

    if isHttp == 'HTTP':
        httpurl = 'http' + "://" + server + ":" + httpPort + filelisturl
    else:
        httpurl = 'https' + "://" + server + ":" + httpsPort + filelisturl

    return httpurl


def getFileUrl( filename ):

    version = param['VERSION']
    reqtype = param['REQTYPE']
    isHttp = param['URLTYPE']


    server = proxyDic['PROXYSERVER']
    idx = proxyDic['PROXYPORT'].find(',')
    if idx == -1:
        httpPort = '8080'
        httpsPort = '8443'
    else:
        tmps = proxyDic['PROXYPORT'].split(',')
        for data in tmps:
            if data.find('HTTPS') != -1:
                httpsPort = data.split(':')[1]
            elif data.find('HTTP') != -1:
                httpPort = data.split(':')[1]
            else:
                log.PrintLog("Option PROXYPORT is Incorrect(default: 8080, 8443")
                httpPort = "8080"
                httpsPort = "8443"

    cnt = 0
    # 전체 DB 받는 Url  만들기
    fileurl = GetFileUrl

    if reqtype == 'LA' or reqtype == 'LP' or reqtype == 'A' or reqtype == 'P':
        # 전체 디비를 받는곳
        fileurl = fileurl.replace('$VERSION', version)
        fileurl = fileurl.replace('$FILENAME', filename)
    else:
        # 증분 DB 받는 url 만들기
        fileurl = fileurl.replace('$VERSION', version)
        fileurl = fileurl.replace('$FILENAME', filename)

    if isHttp == 'HTTP':
        httpurl = 'http' + "://" + server + ":" + httpPort + fileurl
    else:
        httpurl = 'https' + "://" + server + ":" + httpsPort + fileurl

    return httpurl

def GetFile( reqtype, filename, name ):

    try :
        filePath = siteDic['DBDIR'] + os.sep + name
        if os.path.exists(filePath) is False:
            os.mkdir(filePath)

        url = getFileUrl(filename)
        fileFullPath = filePath + os.sep + filename
        res = requests.get(url, verify = False, stream=True)
        if res.status_code == 200:
            with open(fileFullPath, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            return True
    except Exception as e :
        log.PrintLog(sys.exc_info()[0])

class GetFileListThread( threading.Thread ):
    def __init__(self, name, cnt ):
        threading.Thread.__init__(self)
        self.name  = name
        self.cnt   = cnt
        # self.alive = True

    def run(self):
        i = 0
        try:
            ext = getExt(param['REQTYPE'])
            url = getFileListUrl(param['URLTYPE'])
            # log.PrintLog(url)
            fileList = []
            cnt = 0
            while i < self.cnt:
                try:
                    res = requests.get(url, timeout=2, verify=False)
                    print(res.text)
                    if res.status_code == 200:
                        if param['REQTYPE'] == 'LA' or param['REQTYPE'] == 'LP' or \
                            param['REQTYPE'] == 'A' or param['REQTYPE'] == 'P':
                            #  전체 DB
                            data = res.text.split('<BR>')
                            filename = data[1]
                            GetFile(param['REQTYPE'], filename, self.name)
                        else:
                            #  증분 DB
                            data = res.text.split('<BR>')
                            num = int(data[0])
                            fileList = data[1].lower().split(ext)
                        if num != 0:
                            for idx in range(num):
                                filename = fileList[idx] + ext
                                retVal = GetFile(param['REQTYPE'], filename, self.name)
                    else:
                        log.PrintLog("GetFileList status code({}:{})".format(res.url, res.text))
                except:
                    pass
                i += 1
        except:
            print("Exception... GetFileList")
        # log.PrintLog("GetFileList thread is END")

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

    # DBTYPE=SITELIST,URLTYPE=HTTP,THREADNUM=2,VERSION=8,REQTYPE=LA
    # DBTYPE=BLKPORTS,URLTYPE=HTTP,THREADNUM=2,VERSION=,REQTYPE=
    def httpTest(self, values):

        threadList = []
        try :
            dataList = values.split(',')

            for data in dataList:
                key, value = data.split('=')
                param[key] = value

            thrCnt = int(param['THREADNUM'])
            if thrCnt <= 0:
                thrCnt = 1

            cnt = int(param['CNT'])
            startTime = time.time()
            for i in range(thrCnt):
                name = "thread-{}".format(i)
                Thr = GetFileListThread(name, cnt)
                threadList.append(Thr)

            for thr in threadList:
                thr.start()

            num = 0
            cnt = len(threadList)
            while True:
                for thr in threadList:
                    if thr.isAlive() is False:
                        num += 1
                if num == cnt :
                    break
                time.sleep(0.5)
            endTime = time.time()
            log.PrintLog("httpTest Time is {}".format( endTime-startTime))
        except Exception, e:
            log.PrintLog("http Test Exception....{}".format(e))
        return endTime - startTime


    def deleteFiles(self):
        filePath = siteDic['DBDIR']
        if os.path.exists(filePath) is True :
            fileList = os.listdir(filePath)
            for filename in fileList:
                full_filename = os.path.join(filePath, filename)
                os.remove(full_filename)

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
        # log.PrintLog(siteDic)
        # log.PrintLog(proxyDic)
        return True

    def refreshOption(self, filename):
        self.option = config.getOption(filename)
        self.getOption()

    def msgHandler(self, msg):
        retVal = None
        try :
            data = msg.split('!')
            if data[0] == 'RELOAD':
                self.getOption(data[1])
            elif data[0] == 'START':
                # START!DBTYPE=SITELIST,URLTYPE=HTTP,THREADNUM=2,VERSION=8,REQTYPE=LA,LDATE=20160501000000,CNT=10
                # START!DBTYPE=BLKPORTS,URLTYPE=HTTP,THREADNUM=2,VERSION=,REQTYPE=
                retVal = self.httpTest(data[1])
                if retVal is None:
                    log.PrintLog("httpTest is InCorrect")
                else:
                    self.sendQue.append(retVal)
            elif data[0] == 'STOP':
                isStop = True
            elif data[0] == 'DELETE':
                self.deleteFiles()
            else:
                log.PrintLog("%s msg is not Define".format(msg))
        except :
            log.PrintLog("%s msg is not Define".format(msg))


    def run(self):
        log.PrintLog("SiteListThread START")
        retVal = self.getOption()
        if retVal is False:
            log.PrintLog("sitelistThr option Parsing is Fial(", self.option, ")")
            self.setAlive(False)

        if os.path.exists(siteDic['DBDIR']) is False:
            os.mkdir(siteDic['DBDIR'])

        while self.alive:
            if len(self.msgQue) <= 0 :
                time.sleep(0.5)
                continue

            data = self.msgQue.popleft()
            if data:
                self.msgHandler(data)

        log.PrintLog("SiteListThread END")





