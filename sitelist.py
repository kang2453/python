import requests
from threading import Thread
import time
import shutil

httpGetFileListUrl = 'http://192.168.207.50:8080/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
httpsGetFileListUrl = 'https://192.168.207.50:8443/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
httpGetFileUrl = 'http://192.168.207.50:8080/70WKDownloader/getFile.aspx?id=webkeeper&pwd=vhvrn755&version=8&filename=SiteList6.db3&uid=filyp123&rcvname=test'
# httpsUrl = 'https://192.168.207.50:8443/aggregate'



#res = requests.get(httpUrl, timeout=5)
#res = requests.get(httpsUrl, verify=False,timeout=5)

cafile='server.wk.somansa.pem'
keyfile='server.wk.somansa.key'
passphrase='pass1234'

ExceptionNum=0


#res = requests.post(httpsUrl,verify=True, cert=(cafile,keyfile))
#res = requests.post(httpsUrl,cert=(cafile,keyfile))

#print(res.headers)
#print(res.headers['content-Type'])
def httpGetFileList(cnt):
    try:
        # print("thread %d start" % cnt )
        #  res = requests.get(httpUrl, timeout=5)
        # res = requests.get(httpsUrl, timeout=5, verify=False)
        
        res = requests.get(httpGetFileListUrl)
        # res = requests.get(httpsGetFileListUrl, verify=False)
        # res = requests.post(httpsUrl,verify=False )
        # print(res.status_code, res.text)
    except:
        print("Exception ...", res )
        # ExceptionNum += 1


def httpsGetFileList(cnt):
    try:
        res = requests.get(httpsGetFileListUrl, verify=False)
        print( res.headers)
        print( res.text)
    except:
        print("Exception...https", res )


def httpGetFile(cnt):
    try:
        filename = 'SiteList6.db3'
        filename += str(cnt)
        print("filename:", filename)
        total = 0
        res = requests.get(httpGetFileUrl, stream=True)
        if res.status_code == 200:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(res.raw, f )
    except:
        print("Exception...", res )
        

def httpTest(cnt):
    # httpGetFileList(cnt)
    httpsGetFileList(cnt)
    # if cnt < 20 :
        # httpGetFile(cnt)



if __name__ == '__main__':
    num = 0
    start = time.time()
    while True:
        # t1 = Thread(target=httpGetFileList, args=(i,))
        # t1.start()
        # t2 = Thread(target=httpsGetFileList, args=(i,))
        # t2.start()
        # t3 = Thread(target=httpGetFile, args=(i,))
        # t3.start()
        # httpGetFile(i)
        
        t = Thread(target=httpTest, args=(num,))
        t.start()
        time.sleep(0.2)
        break
        num += 1
    print("total time :", time.time()-start)
    print("Exception Cnt: ", ExceptionNum)
    
