from utils import *
import time
import sys
import os
import threading
import socket as sck

class Client:

  def __init__(self):
    self.SERVER_IP = '127.0.0.1'
    self.SERVER_PORT = 6969
    self.logged = False
    self.users = []
    self.messages = []
    self.name = ''

    self.rdt = Rdt3()

    self.lock = threading.RLock()
    self.recvThread = threading.Thread(target=self.recvFromServer)
    self.recvThread.start()

  def connect(self, name='', IP='', port=''):
    pass

  def disconnect(self):
    pass

  def sendMessage(self, message):
    # packet = bytes()
    # packet = message.encode()
    # print(packet)
    # self.socks.sendto(packet, (self.SERVER_IP, self.SERVER_PORT))
    with open('../client/tmpToSend', 'wb') as fd:
      fd.write(message.encode())
    self.lock.acquire()
    self.rdt.rdt_send('../client/tmpToSend', (self.SERVER_IP, self.SERVER_PORT))
    self.lock.release()

  def processCommand(self, command):
    self.sendMessage(command)
    # if command[0] != '/':
    # else:
    #   words = command.split()
    #   if (words[0] == '/hello'):
    #     self.connect(name=words[1], IP=words[2], port=words[3])
    #   elif (words[0] == '/bye'):
    #     self.disconnect()
    #   else:
    #     print("Command not availabe")
    #

  def recvFromServer(self):
    '''
    This the Receiver Thread main execution.

    Receives messages with Rdt3 and store it in a tmp file
    It uses Locks to avoid conflicts with the main thread sending packages(with the same socket)
    Also it will define a maximum waitTime for rdt_recv, if not it will hold the lock possibly forever,
    what cannot happen because the client may want to send something to Server.
    '''
    while True:
      try:
        with open('../client/tmpToRecv', 'w+b') as fd:
          self.lock.acquire()
          self.rdt.rdt_recv(fd, 1)
          #
          # Received messages from server: Do something here.
          # fd.seek(0) # to go back to the begin of the file
          # print('received: ' + fd.read().decode())
          #
          self.lock.release()
      except:
        self.lock.release()

  def run(self):
    # Get user input from the keyboard
    user_input = input("$ ")
    self.processCommand(user_input)


client = Client()

while True:
  client.run()
