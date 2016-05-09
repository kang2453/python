# -*- coding: utf-8 -*-
# 2016.05.09 by kang2453
from threading import Thread

import asyncio


@asyncio.coroutine
def client():
	reader, writer = yield from asyncio.streams.open_connection("192.168.207.50", 12345)

	def send(msg):
		print("> "+ msg)
		writer.write((msg+'\n').encode('utf-8'))

	def recv():
		msgback = (yield from reader.readline()).decode('utf-8').rstrip()
		print("< " + msgback )
		return msgback

	recv()
	# send a line
	# send('add 1 2')
	msg = yield from recv()
	# print(msg.decode('utf-8'))
	# send("repeat 5 hello")
	msg = yield from recv()
	# while True:
	# 	msg = yield from recv()
	# 	if msg == 'end':
	# 		break

	writer.close()
	yield from asyncio.sleep(0.5)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(client())
