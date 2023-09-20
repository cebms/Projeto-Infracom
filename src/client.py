from utils import *
import time
import sys
import os
from threading import Thread

SERVER_IP = '127.0.0.1'
SERVER_PORT = 6969

client = Rdt3()

while True:
    to_send = input('$ ')
    with open('../client/tmp', 'wb') as fd:
        if to_send == '/quit':
            break
        fd.write(to_send.encode())
    client.rdt_send('../client/tmp', (SERVER_IP, SERVER_PORT))
