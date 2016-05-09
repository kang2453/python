# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import timeit
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen

urls = ['http://b.ssut.me', 'https://google.com', 'https://apple.com', 'https://ubit.info', 'https://github.com/ssut']

start = 0

def forloop():
	start = timeit.default_timer()
	for url in urls:
	    # print('Start', url)
	    try:
	        urlopen(url)
	    except :
		    print(url , " is Exception")
		    continue
	    print('Done', url)


def fetch(url):
	try:
		urlopen(url)
		print('Done', url)
	except :
		print(url, " is Exception")


def threadExec():
	with ThreadPoolExecutor(max_workers=5) as executor:
		for url in urls:
			executor.submit(fetch, url)

if __name__ == '__main__':
	start = timeit.default_timer()
	# forloop()
	threadExec()
	duration = timeit.default_timer() - start
	print("total : %d" % duration)