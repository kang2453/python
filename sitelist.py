# -*- coding: utf-8 -*-

import time

from Main import getOption

TYPE = 'http'
HOST = '192.168.207.50'
PORT = 8080

ALIVE = True


# httpGetFileListUrl  = 'http://192.168.207.50:8080/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpsGetFileListUrl = 'https://192.168.207.50:8443/70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
# httpGetFileUrl      = 'http://192.168.207.50:8080/70WKDownloader/getFile.aspx?id=webkeeper&pwd=vhvrn755&version=8&filename=SiteList6.db3&uid=filyp123&rcvname=test'

GetFileListUrl ='70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='
GetFileUrl     = '70WKDownloader/getFileList.aspx?id=webkeeper&pwd=vhvrn755&version=8&reqtype=LM&uid=fpwlkb0&rcvname=wkAgent&ldate=20160125164427&SN='







def alive(type):
	print("SiteList Alive END")
	ALIVE = type

def getOption(option):
	return True

def main(option, ):
	print("sitelist Dic: ", option['sitelist'])
	rv = getOption(option)
	if rv is False:
		print("SiteList Thr option parsing Error")
		SystemExit(0)

	cnt = 0
	while ALIVE:
		print("sitelist main ", cnt)
		cnt += 1
		if cnt == 10 :
			break
		time.sleep(1)

	print("SiteList Thread END!!!")


#f __name__ == "__main__":
	#main(option, Que)