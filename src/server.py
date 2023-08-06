from utils import *
import socket as sck
import time

MY_IP = '127.0.0.1'
PORT = 6969

server = UDP()
server.socks.bind((MY_IP, PORT))

while True:
  print("Waiting for files...")
  data, ret_addr = server.recv_file()
  if len(data) != 0:
    fd = open('../server/received_file', 'wb')
    fd.write(data)
    fd.close()
    server.send_file('../server/received_file', ret_addr)