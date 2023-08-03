import socket as sck
import time

MY_IP = '127.0.0.1'
PORT = 6969

def recv_file(socks):
    data_total = bytes()
    while 1:
        my_other_socks.settimeout(3)
        try:
            data, addr = my_other_socks.recvfrom(1024)
            data_total += data
        except sck.timeout:
            break
    return data_total

my_other_socks = sck.socket(sck.AF_INET,
                      sck.SOCK_DGRAM)
my_other_socks.bind((MY_IP, PORT))

data = recv_file(my_other_socks)
fd = open('file_recv.txt', 'wb')
fd.write(data)
fd.close()
data = recv_file(my_other_socks)
fd = open('messi_retorno.jpeg', 'wb')
fd.write(data)
fd.close()

