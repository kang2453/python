# -*- coding: utf-8 -*-

from socket import *

import os

msg =""

ADDR=('192.168.207.50',10001)
BUFSIZE=1024
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)

data = "START|sitelist"
sock.send(data.encode('utf-8'))
msg = sock.recv(BUFSIZE)

print("Recv Msg: ", msg.decode('utf-8') )

sock.close()