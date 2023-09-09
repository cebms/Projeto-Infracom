from utils import *
import time
import sys
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 6969

args = sys.argv

if len(args) < 2:
  print('Pass the name of the file to send on command line')

file_name = args[1]

client = Rdt3()

client.rdt_send(os.path.join('../client', file_name), (SERVER_IP, SERVER_PORT))
print('arquivo enviado com sucesso')

with open(('../client/receivedFiles/' + file_name), 'wb') as fd:
  client.rdt_recv(fd)
  print('arquivo recebido com sucesso')
