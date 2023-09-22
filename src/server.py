from typing import TextIO
from utils import Rdt3
from utils import User
from utils import Message
import socket as sck
import time
import copy


class Server:

  def __init__(self, IP, port):
    self.IP = IP
    self.port = port
    #self.rdt = Rdt3((self.IP, self.port))
    self.users = []
    self.messages = []
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

  def listUsers(self, _):
    usernamesList = []
    for user in self.users:
      usernamesList.append(user.name)

    print(usernamesList)
    return usernamesList

  def disconnectUser(self, *args):
    params = args[0]
    #params = [name]
    usersCopy = self.users[:]
    for userCopy in usersCopy:
      if params[0] == userCopy.name:
        self.users.remove(userCopy)
        print("User " + params[0] + " Disconected!")
        return True

    print("User " + params[0] + " not found!")
    return False

  def connectUser(self, *args):
    params = args[0]
    #params = [name, ip, port]
    contains = False
    for user in self.users:
      if (user.name == params[0]):
        contains = True
        break
    if not contains:
      newUser = User(name=params[0], IP=params[1], port=params[2])
      self.users.append(newUser)
      print("User " + params[0] + " logged in!")
      return True
    else:
      print("User " + params[0] + " Already Logged!")
      return False

  def banUser(self, **kwargs):
    pass

# considerando que temos nome-IP-porta-mensagem (nessa ordem e separdo por espacos)

  def getMessage(self, *args):
    params = args[0]

    text = params
    name = ''
    IP = ''
    port = 0
    i = 0

    # Get Name
    while i < len(text) and text[i] != '-':
      name = name + text[i]
      i = i + 1

    if i < len(text):
      i = i + 1  # Move past the '-'
    else:
      print("Wrong message format!")
      return False

    # Get IP
    while i < len(text) and text[i] != '-':
      IP = IP + text[i]
      i = i + 1

    if i < len(text):
      i = i + 1  # Move past the '-'
    else:
      print("Wrong message format!")
      return False

    # Get Port
    while i < len(text) and text[i] != '-':
      port = port * 10 + int(text[i])
      i = i + 1

    if i < len(text):
      i = i + 1  # Move past the '-'
    else:
      print("Wrong message format!")
      return False

    message = text[i:]

    # create objcts and append to others
    newMessage = Message(User(name, IP, port), message)
    self.messages.append(newMessage)
    print('message received from ' + name + '!')
    return True

  def runCommand(self, command, args):
    method = self.commands[command]
    return method(args)

  def processCommand(self, command):
    if command[0] != '/':
      self.runCommand("message", command)
    else:
      words = command.split()
      self.runCommand(words[0], words[1:])


# instanciacao do server
server = Server('127.0.0.1', 6969)

socks = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
socks.bind(('127.0.0.1', 6969))

while True:
  data, addr = socks.recvfrom(1024)
  print(data.decode())
  server.processCommand(data.decode())

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
