# -*- coding: utf-8 -*-

from threading import Thread
import time
import asyncio
import socket

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

	# send a line
	send('add 1 2')
	msg = yield from recv()

	send("repeat 5 hello")
	msg = yield from recv()
	while True:
		msg = yield from recv()
		if msg == 'end':
			break

	writer.close()
	yield from asyncio.sleep(0.5)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(client())
