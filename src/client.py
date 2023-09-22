from utils import *
import time
import sys
import os
from threading import Thread
import socket as sck


class Client:

  def __init__(self):
    self.SERVER_IP = '127.0.0.1'
    self.SERVER_PORT = 6969
    self.logged = False
    #self.rdt = UDP()
    self.users = []
    self.messages = []
    self.name = ''
    #TODO mudar para RDT
    self.socks = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

  def connect(self, name='', IP='', port=''):
    pass

  def disconnect(self):
    pass

  def sendMessage(self, message):
    packet = bytes()
    packet = message.encode()
    print(packet)
    self.socks.sendto(packet, (self.SERVER_IP, self.SERVER_PORT))

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

  def run(self):
    # Get user input from the keyboard
    user_input = input("$ ")
    self.processCommand(user_input)


client = Client()

while True:
  client.run()
