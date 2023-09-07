from utils import *
import socket as sck
import time

MY_IP = '127.0.0.1'
PORT = 6969
rdt = Rdt3((MY_IP, PORT))

with open('../server/received_file', 'wb') as file:
  rdt.rdt_recv(file)

  print('arquivo recebido com sucesso')
#while True:
#  print("Waiting for files...")
#  data, ret_addr = server.data()
#  if len(data) != 0:
#    fd = open('../server/received_file', 'wb')
#    fd.write(data)
#    fd.close()
#    server.send_file('../server/received_file', ret_addr)
