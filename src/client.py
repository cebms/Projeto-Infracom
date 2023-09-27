from utils import *
import sys
import threading

class Client:

  def __init__(self):
    self.SERVER_IP = '127.0.0.1'
    self.SERVER_PORT = 6969
    self.friends = []
    self.commands = {
      "/addtomylist": self.addUser,
      "/rmvfrommylist": self.removeUser,
      "/mylist": self.listFriends
    }

    self.rdt = Rdt3()

    self.lock = threading.RLock()
    self.recvThread = threading.Thread(target=self.recvFromServer)
    self.recvThread.start()

  def addUser(self, *args):
    if(self.logged): #TODO verificar se o nome existe
        user_name = args[0][0]
    else:
        print("You should log in before send messages, try: /hello <your_name>")
  
  def removeUser(self, user):
    pass
  
  def listFriends(self):
    for friend in self.friends:
      print("-> ", friend)

  def sendMessage(self, message):
    self.lock.acquire()
    self.rdt.rdt_sendBytes(message.encode(), (self.SERVER_IP, self.SERVER_PORT))
    self.lock.release()

  def processCommand(self, text):
    commands = text.split()
    if commands[0] in self.commands.keys():
      method = self.commands[commands[0]]
      method(commands[1:])
    else:
        self.sendMessage(text)

  def recvFromServer(self):
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
    '''
    while True:
      try:
        with open('../client/tmpToRecv', 'w+b') as fd:
          self.lock.acquire()
          self.rdt.rdt_recv(fd, 1)
          # Received messages from server: Do something here.
          fd.seek(0) # to go back to the begin of the file
          print('\033[2K' + '\033[2D', end='')
          msg = fd.read().decode()
          self.processIncomingMessage(msg)
          print(msg[3:])
          print('$ ', end='')
          sys.stdout.flush()
          #
          self.lock.release()
      except:
        self.lock.release()

  def processIncomingMessage(self, msg):
    if msg[1] == '1':
      self.logged = False
    elif msg[1] == '2':
      self.logged = True

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
print('$ ', end='')
while True:
  client.run()
