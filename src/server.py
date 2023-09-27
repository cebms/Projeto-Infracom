from typing import TextIO
from utils import Rdt3
from utils import User
from utils import Message
import socket as sck
import time
import copy
import random

greetings = ['A wild {} {} {} appeared!', 'Welcome {} {} {}!', '{} {} {} jumped into the chat']

class Server:

  def __init__(self, IP, port):
    self.IP = IP
    self.port = port
    self.rdt = Rdt3((self.IP, self.port))
    self.messages = []
    self.users = {}
    self.commands = {
        "/hello": self.connectUser,
        "/bye": self.disconnectUser,
        "/list": self.listUsers,
        "/ban": self.banUser,
        "message": self.getMessage
    }

  def showMessages(self):
    for message in self.messages:
      message.show()

  def listUsers(self, *args):
    usernamesList = []
    for user in self.users.values():
      print(user)
      usernamesList.append(user)

    return usernamesList

  def disconnectUser(self, *args):
    userAddr = args[0]

    if userAddr in self.users:
      name = self.users[userAddr]
      print('User ' + name + ' disconnected')
      message = '{} {} {} disconected.'.format(userAddr[0], userAddr[1], name)

      ### sending the end of conection to the one who requested it
      with open('../server/tmpFile', 'w+b') as fd:
        fd.write(message.encode())
      self.rdt.rdt_send('../server/tmpFile', userAddr)

      self.users.pop(userAddr)
      return message
    else:
      print('User was not logged in')
      return None

  def connectUser(self, *args):
    name = args[0][0]
    userAddr = args[1]

    if userAddr in self.users.keys():
      print("User " + name + " Already Logged!")
      return None
    else:
      if name not in self.users.values():
        print("User " + name + " logged in!")
        self.users[userAddr] = name
        return random.sample(greetings, 1)[0].format(userAddr[0], userAddr[1], name)
      else:
        print('Someone already has this name')
        return None

  def banUser(self, *args):
    pass

# considerando que temos nome-IP-porta-mensagem (nessa ordem e separdo por espacos)

  def getMessage(self, *args):

    message = args[0]
    userAddr = args[1]

    if userAddr in self.users:
      # create objcts and append to others
      name = self.users[userAddr]
      newMessage = Message(User(name, userAddr[0], userAddr[1]), message)
      self.messages.append(newMessage)
      print('message received from ' + name + ': ' + message)
      return '{} {} {}: {}'.format(userAddr[0], userAddr[1], name, message)
    else:
      print('Someone that is not logged in sent a message')
      return None

  def runCommand(self, command, text, retAddr):
    if command not in self.commands:
      print('Command does not exist')
      # return self.getMessage(text, retAddr) #if dont exist, it's a message!
      return None
    method = self.commands[command]
    return method(text, retAddr)

  def processCommand(self, command, retAddr):
    if command[0] != '/':
      return self.runCommand("message", command, retAddr)
    else:
      words = command.split()
      if words[0] == '/bye':
        return self.disconnectUser(retAddr)
      else:
        return self.runCommand(words[0], words[1:], retAddr)

# instanciacao do server
server = Server('127.0.0.1', 6969)

# socks = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
# socks.bind(('127.0.0.1', 6969))

while True:
  # data, addr = socks.recvfrom(1024)
  # print(data.decode())
  with open('../server/tmpFile', 'w+b') as fd:
    ret_addr = server.rdt.rdt_recv(fd)
    fd.seek(0)
    message = fd.read().decode()
    #print(message)
  messageBack = server.processCommand(message, ret_addr)

  #sending back the message to client
  fd = open('../server/tmpFile', 'wb')
  if messageBack == None:
    fd.write('Bad Request, try again'.encode())
    fd.close()
    server.rdt.rdt_send('../server/tmpFile', ret_addr) #sending to just one client, that sent somthing wrong
  else:
    fd.write(messageBack.encode())
    fd.close()
    for users in server.users: #broadcast send
      server.rdt.rdt_send('../server/tmpFile', users)

# validacao de comandos
# server.processCommand('/hello thiago 127.0.0.1 6968')
# server.processCommand('/hello icaro 127.0.0.1 6968')
# server.processCommand('/hello jorge 127.0.0.1 6968')
# server.processCommand('/list')
# server.processCommand('/hello icaro 127.0.0.1 6968')
# server.processCommand('/list')
# server.processCommand('/bye thiago 127.0.0.1 6968')
# server.processCommand('/list')
# server.processCommand("Thiago-127.0.0.1-6968-minha mensagem eh essa!")
# server.processCommand("Rodrigo-127.0.0.1-6968-beleza então, chau")
# server.showMessages()

#print(server.runCommand(command="/list"))

# with open('../server/history.txt', 'wb') as hs:
#   while True:
#     with open('../server/received_file', 'w+b') as message:
#       ret_addr = rdt.rdt_recv(message)
#       if ret_addr not in users:
#         users[ret_addr] = id
#         id += 1
#       message.seek(0)
#       print((str(users[ret_addr]) + ': ' + message.read().decode()).encode())
