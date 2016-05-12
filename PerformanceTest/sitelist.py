# -*- coding: utf-8 -*-

import os
import time
import log
import threading
import requests
import shutil
import config

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

def getUrl( ishttp, type, filelist ):
    urllist = []

    version = param['VERSION']
    reqtype = param['REQTYPE']
    ldate = param['LDATE']
    ishttp = param['URLTYPE']


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

    if type == 'getfilelist':
        filelisturl =  GetFileListUrl
        filelisturl = filelisturl.replace('$VERSION', version)
        filelisturl = filelisturl.replace('$REQTYPE', reqtype)
        filelisturl = filelisturl.replace('$LDATE', ldate)

        httpFullUrl = 'http' + "://" + server + ":" + httpPort + filelisturl
        httpsFullUrl = 'https' + "://" + server + ":" + httpsPort + filelisturl

        if ishttp == 'HTTP':
            urllist.append(httpFullUrl)
        elif ishttp == 'HTTPS':
            urllist.append(httpsFullUrl)

    elif type == 'getfile':
        cnt = 0
        # 전체 DB 받는 Url  만들기
        if reqtype == "LA" or reqtype == "LP" or reqtype =="A" or reqtype == "P" :
            filename = filelist
            fileurl = GetFileUrl

            if reqtype.find('L') == -1:
                ext = ".ifo"
            else:
                ext = ".db3"

            fileurl = fileurl.replace('$VERSION', version)
            fileurl = fileurl.replace('$FILENAME', filename + ext)

            httpFullUrl = 'http' + "://" + server + ":" + httpPort + fileurl
            httpsFullUrl = 'https' + "://" + server + ":" + httpsPort + fileurl

            if ishttp == 'HTTPS':
                urllist.append(httpsFullUrl)
            elif ishttp == 'HTTP':
                urllist.append(httpFullUrl)
        else:
            # 증분 DB 받는 url 만들기
            for filename in filelist:
                if filename == '':
                    continue

                fileurl = GetFileUrl

                if reqtype.find('L') == -1:
                    ext = ".ifo"
                else :
                    ext = ".db3"


                fileurl = fileurl.replace('$VERSION', version)
                fileurl = fileurl.replace('$FILENAME', filename+ext)

                httpFullUrl = 'http' + "://" + server + ":" + httpPort + fileurl
                httpsFullUrl = 'https' + "://" + server + ":" + httpsPort + fileurl

                if ishttp == 'HTTPS':
                    urllist.append(httpsFullUrl)
                elif ishttp == 'HTTP':
                    urllist.append(httpFullUrl)

                cnt += 1

    return urllist



def GetFile( type, fileList ):

    log.PrintLog(fileList)
    filePath = siteDic['DBDIR']
    urlList = getUrl(type, 'getfile', fileList)

    if len(urlList) > 0 :
        log.PrintLog("urlList num: {}".format(len(urlList)))
        i =0
        for url in urlList:
            # log.PrintLog("{} filename = {}".format(i, fileList[i]))
            fileFullPath = filePath + os.sep +  fileList[i]+'.db3'
            res = requests.get(url, stream=True)
            if res.status_code == 200:
                with open(fileFullPath, 'wb') as f:
                    shutil.copyfileobj(res.raw, f )
            i += 1



def GetFileList(name, cnt):
    i = 0
    global param
    try:
        urlList = []
        urlList = getUrl(param['URLTYPE'], 'getfilelist', None)
        # log.PrintLog(httpFullUrl)
        # log.PrintLog(httpsFullUrl)
        tmp = ""
        num = 0
        fileList = []
        while i < cnt:
            try :
                if len(urlList) >= 0:
                    res = requests.get(urlList[0], timeout=2, verify=False)
                    if res.status_code == 200:
                        if param['REQTYPE'] == 'LA' or param['REQTYPE'] == 'LP':
                            data = res.text.split('<BR>')
                            tmp = data[0]
                            num = int(tmp[:1])
                            fileList = data[1]
                        else:
                            data = res.text.split('<BR>')
                            num = int(data[0])
                            if param['REQTYPE'].find('L') == -1:
                                ext = ".ifo"
                            else:
                                ext = ".db3"
                            fileList = data[1].lower().split(ext)

                        if num != 0:
                            GetFile(type, fileList)
                else:
                    log.PrintLog("GetFileList status code({}:{})".format(res.url, res.text))
            except :
                pass
            i += 1
    except:
        print("Exception... GetFileList" )
        return


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
        dataList = values.split(',')

        for data in dataList:
            key, value = data.split('=')
            param[key] = value

        thrCnt = int(param['THREADNUM'])
        if thrCnt <= 0:
            thrCnt = 1

        cnt = int(param['CNT'])
        for i in range(thrCnt):
            name = "thread-{}".format(i)
            t = threading.Thread(target=GetFileList, args=(name, cnt))
            t.name = name
            threadList.append(t)

        startTime = time.time()
        for id in threadList:
            id.start()

        for id in threadList:
            id.join()

        endTime = time.time()
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
        log.PrintLog(siteDic)
        log.PrintLog(proxyDic)
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





