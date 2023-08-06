from utils import *
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 6969

client = UDP()

# Altere aqui o arquivo que deseja enviar
file_name = 'imageToSend.jpeg' 
# file_name = 'file.txt'

client.send_file('../client/' + file_name, (SERVER_IP, SERVER_PORT))

time.sleep(1)
data, _ = client.recv_file()
if len(data) != 0:
  fd = open('../client/receivedFiles/' + file_name, 'wb')
  fd.write(data)
  fd.close()