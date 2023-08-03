import socket as sck
import os
import math as m
import time

MESSAGE = b'hello ma bro'
UDDP_IP = '127.0.0.1'
PORT = 6969

def send_file(file_name):
    file = open(file_name, 'rb')

    while(1):
        data = file.read(1024)
        if len(data) == 0:
            break
        my_socks.sendto(data, (UDDP_IP, PORT))

    file.close()


my_socks = sck.socket(sck.AF_INET,
                      sck.SOCK_DGRAM)

send_file('file.txt')
time.sleep(4)
send_file('messiiiiiii.jpeg')
