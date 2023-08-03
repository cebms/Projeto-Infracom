import socket as sck
import time

MY_IP = '127.0.0.1'
PORT = 6969

my_other_socks = sck.socket(sck.AF_INET,
                      sck.SOCK_DGRAM)
my_other_socks.bind((MY_IP, PORT))

while 1:
    data, addr = my_other_socks.recvfrom(1024)
    print(data)
    #print(addr)

    time.sleep(1)
