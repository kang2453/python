# -*- coding: utf-8 -*-

import time

HOST = None
PORT = None

ALIVE = True


def alive(type):
    print("Socket Alive END")
    ALIVE = type



def main(option, Que):
    cnt = 0
    while ALIVE:
        #print("socket main ", cnt)
        cnt += 1
        if cnt == 10 :
            break
        time.sleep(1)
    #print("Socket Thread END!!!")

if __name__ == "__main__":
    main(option, Que)
