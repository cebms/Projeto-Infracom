from utils import *
import socket as sck
import time

MY_IP = '127.0.0.1'
PORT = 6969
rdt = Rdt3((MY_IP, PORT))
ret_addr = ()
with open('../server/received_file', 'wb') as file:
  ret_addr = rdt.rdt_recv(file)
  print('arquivo recebido com sucesso')

print("Transmitindo de volta para ", ret_addr)

rdt.rdt_send('../server/received_file', ret_addr)
print('arquivo transmitido com sucesso')
