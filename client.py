import socket as sck
import os
import math as m

MESSAGE = b'hello ma bro'
UDDP_IP = '127.0.0.1'
PORT = 6969

my_socks = sck.socket(sck.AF_INET,
                      sck.SOCK_DGRAM)

file_info = os.stat('file.txt')
tam = file_info.st_size / 1024
bytes_for_id = m.ceil((m.log2(tam) / 8))

file = open('file.txt', 'rb')
file.seek(0)

cnt = 0
while(1):
    data = file.read(1024 - bytes_for_id)
    if len(data) == 0:
        break
    data = data + cnt.to_bytes(bytes_for_id, byteorder='big')
    my_socks.sendto(data, (UDDP_IP, PORT))
    cnt += 1

file.close()
