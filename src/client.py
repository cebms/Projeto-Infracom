from utils import *
import sys
import threading, tty, termios
import re
import time

class Client:

  def __init__(self):
    self.SERVER_IP = '127.0.0.1'
    self.SERVER_PORT = 6969
    self.friends = []
    self.logged_users = []
    self.commands = {
      "/add": self.addUser, #addtomylist
      "/rmv": self.removeUser, #rmvfrommylist 
      "/ml": self.listFriends #mylist
    }
    self.writed = ''

    self.rdt = Rdt3()

    self.lock = threading.Lock()
    self.recvThread = threading.Thread(target=self.recvThreadExecution)
    self.recvThreadRun = True
    self.recvThread.start()

  def printUserInput(self):
    print('\r$ ' + self.writed, end='')
    sys.stdout.flush()

  def fetchLoggedList(self):
    fd = open('../client/tmpToRecv', 'w+b')
    try:
      self.lock.acquire()
      self.sendMessageWithoutLock('/list')
      self.rdt.rdt_recv(fd, 5)
      self.lock.release()
    except:
      if self.lock.locked():
        self.lock.release()
      fd.close()
      print('Could not fetch logged list')
      return False

    fd.seek(0)
    message = fd.read().decode()
    self.logged_users = message[3:].split(',')
    fd.close()
    return True

  def addUser(self, *args):
    if not self.fetchLoggedList():
      return False

    if(self.logged): #TODO verificar se o nome existe
        user_name = args[0][0]
        if user_name in self.logged_users:
            print("User " + user_name + " added to your list!")
            self.friends.append(user_name)
        else:
            print('\033[2K', end='') #clean line
            print("User not found.")
    else:
        print("You should log in before send messages, try: /hi <your_name>")

    self.printUserInput()
    return True
  
  def removeUser(self, *args):
    friendToRemove = args[0][0]

    if self.logged:
      if friendToRemove in self.friends:
        self.friends.remove(friendToRemove)
        print('{} removed succesfully!'.format(friendToRemove))
      else:
        print('\033[2K', end='') #clean line
        print('Friend not found')
    else:
        print("You should log in before send messages, try: /hi <your_name>")

    self.printUserInput()
    return True

  def listFriends(self):
    if not self.fetchLoggedList():
      return False

    if not self.friends:
      print('You do not have friends, i am sorry...')
      self.printUserInput()
      return True

    print('\033[2K', end='') #clean line
    print(blue('Friends List:'))
    for friend in self.friends:
      print(green('(Online) ') if friend in self.logged_users else red('(Offline) '), end='')
      print(friend)
    self.printUserInput()
    return True

  def sendMessageWithoutLock(self, message):
    return self.rdt.rdt_sendBytes(message.encode(), (self.SERVER_IP, self.SERVER_PORT))

  def sendMessage(self, message):
    self.lock.acquire()
    status = self.sendMessageWithoutLock(message)
    self.lock.release()
    return status

  def processCommand(self, text):
    commands = text.split()
    if commands[0] in self.commands.keys():
      method = self.commands[commands[0]]
      if commands[0] == '/ml':
        return method()
      else:
        if not commands[1:]:
          print('Missing command arguments')
        else:
          return method(commands[1:])
    else:
        return self.sendMessage(text)


  def recvThreadExecutionStop(self):
    self.recvThreadRun = False

  def recvThreadExecution(self):
    '''
    This the Receiver Thread main execution.

    Receives messages with Rdt3 and store it in a tmp file
    It uses Locks to avoid conflicts with the main thread sending packages(with the same socket)
    Also it will define a maximum waitTime for rdt_recv, if not it will hold the lock possibly forever,
    what cannot happen because the client may want to send something to Server.
    '''
    '''
    #0 -> Normal (chat) message
    #1 -> Not logged message
    #2 -> Login success
    #3 -> Command not found error
    #4 -> Logged users list
    #5 -> Info Message
    '''
    while self.recvThreadRun:
      fd = open('../client/tmpToRecv', 'w+b')
      try:
        self.lock.acquire()
        self.rdt.rdt_recv(fd, 1)
        self.lock.release()
          # Received messages from server: Do something here.
      except:
        if self.lock.locked():
          self.lock.release()
      fd.seek(0) # to go back to the begin of the file
      msg = fd.read().decode()
      if not msg:
        continue
      msg = self.processIncomingMessage(msg)
      print('\r\033[2K', end='')
      print(msg[3:])
      self.printUserInput()

  def processIncomingMessage(self, msg):
    if msg[1] == '1':
      self.logged = False
    elif msg[1] == '2':
      self.logged = True
    elif msg[1] == '4':
      self.logged_users = msg[3:].split(',')
    elif msg[1] == '0':
      pattern = r'~(.*?):'
      correspondences = re.findall(pattern, msg)
      user_name = correspondences[0]
      if user_name[:-4] in self.friends:
        msg = msg[:3] + yellow('[Friend] ') + msg[3:]
        
    return msg

  def read_input(self):
    fd = sys.stdin.fileno()
    ch = 0
    while True:
      try:
          old_settings = termios.tcgetattr(fd)
          tty.setraw(sys.stdin.fileno())
          ch = sys.stdin.read(1)
      finally:
          termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
          if ord(ch) == 13:
            print('')
            ret = self.writed
            self.writed = ''
            return ret
          elif ord(ch) == 127:  #delete a char
            if self.writed: #only delete if has chars to delete
              print('\033[1D \033[1D', end='')
              sys.stdout.flush()
              self.writed = self.writed[:-1]
          else:
            self.writed += ch
            print(ch, end='')
            sys.stdout.flush()

  def run(self):
    # Get user input from the keyboard
    user_input = self.read_input()
    if len(user_input) == 0:
      return True
    if user_input == '/q':
      return False
    print('\033[1A' + '\033[2K', end='')
    print('Waiting for server...')
    print('\033[1A' + '\033[2D', end='')
    if not self.processCommand(user_input):
      print('\r\033[2K', end='')
      print('Connection Failed')
      self.printUserInput()
    return True

client = Client()
client.printUserInput()
while client.run():
  None

client.recvThreadExecutionStop()
