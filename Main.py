# -*- coding: utf-8 -*-
import codecs
import threading
import time




import sock
import sitelist

Option = {}

cmddic   = {}
proxydic  = {}
sitedic   = {}

# thread 객체 담을곳
threads = []

g_alive = True

def ParsingOption(type, msg):
	tmp = msg.split('=')
	if len(tmp) == 2:
		if type =='cmd':
			cmddic[tmp[0]] = tmp[1]
		elif type == 'proxy':
			proxydic[tmp[0]] = tmp[1]
		elif type == 'sitelist':
			sitedic[tmp[0]] = tmp[1]


def getOption():
	with codecs.open('config.txt', 'r', encoding='utf-8') as f:
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

def gAlive(type):
	g_alive = type

def main():
	#ue = Queue( maxsize = 1000 )
	siteThr = threading.Thread(target=sitelist.main, args=(Option, ))
	sockThr = threading.Thread(target=sock.main, args=(Option,))

	siteThr.daemon = True
	sockThr.daemon = True

	siteThr.start()
	sockThr.start()

	# threads.append(sockThr)
	# threads.append(siteThr)

	# for th in threads:
	# 	th.join()

	cnt = 0
	while g_alive:
		print("main while", cnt )
		if cnt == 2:
			# gAlive(False)
			sitelist.alive(False)
			sock.alive(False)
			break
		cnt += 1
		time.sleep(1)


if __name__ == "__main__":
	getOption()
	# print('cmd: ', Option['cmddic'])
	# print('proxy: ', Option['proxydic'])
	# print('sitelist: ', Option['sitedic'])
	main()
	time.sleep(2)
	print("END")
