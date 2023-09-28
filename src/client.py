from utils import *
import sys
import threading

class Client:

  def __init__(self):
    self.SERVER_IP = '127.0.0.1'
    self.SERVER_PORT = 6969
    self.friends = []
    self.logged_users = []
    self.commands = {
      "/addtomylist": self.addUser,
      "/rmvfrommylist": self.removeUser,
      "/mylist": self.listFriends
    }

    self.rdt = Rdt3()

    self.lock = threading.Lock()
    self.recvThread = threading.Thread(target=self.recvThreadExecution)
    self.recvThreadRun = True
    self.recvThread.start()

  def printUserInput(self):
    print('$ ', end='')
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
      return

    fd.seek(0)
    message = fd.read().decode()
    self.logged_users = message[3:].split(',')
    fd.close()

  def addUser(self, *args):
    self.fetchLoggedList()

    if(self.logged): #TODO verificar se o nome existe
        user_name = args[0][0]
        if user_name in self.logged_users:
            print("User " + user_name + " added to your list!")
            self.printUserInput()
            self.friends.append(user_name)
        else:
            print('\033[2K', end='') #clean line
            print("User not found.")
            self.printUserInput()
    else:
        print("You should log in before send messages, try: /hi <your_name>")
  
  def removeUser(self, user):
    pass
  
  def listFriends(self):
    self.fetchLoggedList()

    if not self.friends:
      print('You do not have friends, i am sorry...')
      self.printUserInput()
      return

    print('\033[2K', end='') #clean line
    print('Friends List:')
    for friend in self.friends:
      print('(Online) ' if friend in self.logged_users else '(Offline) ', end='')
      print(friend)
    self.printUserInput()

  def sendMessageWithoutLock(self, message):
    self.rdt.rdt_sendBytes(message.encode(), (self.SERVER_IP, self.SERVER_PORT))

  def sendMessage(self, message):
    self.lock.acquire()
    self.sendMessageWithoutLock(message)
    self.lock.release()

  def processCommand(self, text):
    commands = text.split()
    if commands[0] in self.commands.keys():
      method = self.commands[commands[0]]
      if commands[0] == '/mylist':
        method()
      else:
        method(commands[1:])
    else:
        self.sendMessage(text)


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
    #0 -> Normal message
    #1 -> Not logged message
    #2 -> Login success
    #3 -> Command not found error
    #4 -> Logged users list
    '''
    while self.recvThreadRun:
      try:
        with open('../client/tmpToRecv', 'w+b') as fd:
          self.lock.acquire()
          self.rdt.rdt_recv(fd, 1)
          # Received messages from server: Do something here.
          fd.seek(0) # to go back to the begin of the file
          print('\033[2K' + '\033[2D', end='')
          msg = fd.read().decode()
          print(msg[3:])
          self.printUserInput()
          self.lock.release()

          self.processIncomingMessage(msg)
      except:
        self.lock.release()

  def processIncomingMessage(self, msg):
    if msg[1] == '1':
      self.logged = False
    elif msg[1] == '2':
      self.logged = True
    elif msg[1] == '4':
      self.logged_users = msg[3:].split(',')

  def run(self):
    # Get user input from the keyboard
    user_input = input()
    if len(user_input) == 0:
      return True
    print('\033[1A' + '\033[2K', end='')
    print('Waiting for server...')
    print('\033[1A' + '\033[2D', end='')
    self.processCommand(user_input)

client = Client()
client.printUserInput()
while True:
  client.run()
