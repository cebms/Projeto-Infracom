from typing import TextIO
from utils import Rdt3
from utils import User
from utils import Message
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
        "/hi": self.connectUser,
        "/bye": self.disconnectUser,
        "/list": self.listUsers,
        "/ban": self.banUser,
        "/voteban": self.voteBan,
        "message": self.getMessage
    }
    self.ban_votes = {}  # Dicionário para rastrear os votos de banimento
    self.ban_threshold = 0  # Limiar necessário para banir um usuário
    self.ban_target = None  # Usuário alvo para banimento

  def showMessages(self):
    for message in self.messages:
      message.show()

  def listUsers(self, *args):
    usernamesList = ''
    usernamesList = ",".join(self.users.values())
    #sending as runtimeError to send exclusivelly to the person who typed the command
    #fix it.
    raise RuntimeError("#4 " + usernamesList)

  def disconnectUser(self, *args):
    userAddr = args[0]

    name = self.users[userAddr]
    print('User ' + name + ' disconnected')
    message = '{} {} {} disconected.'.format(userAddr[0], userAddr[1], name)
    message = "#1 " + message
    ### sending the end of conection to the one who requested it
    self.rdt.rdt_sendBytes(message.encode(), userAddr)

    self.users.pop(userAddr)
    return message

  def connectUser(self, *args):
    if not args[0]:
        raise RuntimeError("#3 Usage: /hello <username>")

    name = args[0][0]
    userAddr = args[1]

    if userAddr in self.users.keys():
      print("User " + self.users[userAddr] + " already logged!")
      raise RuntimeError("#1 You already have an account logged in")
    else:
      if name not in self.users.values():
        print("User " + name + " logged in!")
        self.users[userAddr] = name
        return "#2 " + random.sample(greetings, 1)[0].format(userAddr[0], userAddr[1], name)
      else:
        print('Someone already has this name')
        raise RuntimeError("#1 Someone is using this name, try another")

  def banUser(self, *args):
    if not args[0]:
        raise RuntimeError("#3 Usage: /ban <username>")
    
    userAddr = args[1]    
    username_to_ban = args[0][0]
    if username_to_ban in self.users.values():
        if username_to_ban == self.ban_target:
            raise RuntimeError("#1 You have already initiated a ban vote for this user.")
        
        self.ban_votes.clear()  # Limpar os votos anteriores
        self.ban_votes[self.users[userAddr]] = True  # O usuário que iniciou a votação vota automaticamente
        self.ban_target = username_to_ban
        self.ban_threshold = len(self.users) // 2 + 1  # Mais da metade dos usuários conectados
        
        # Enviar uma mensagem para todos os usuários do chat informando a votação de banimento
        ban_message = "#0 [Server] {} initiated a ban vote for user {}. Vote using /voteban <yes/no>.".format(self.users[userAddr], username_to_ban)
        return ban_message
    else:
        raise RuntimeError("#1 User not found: {}".format(username_to_ban))

  def voteBan(self, *args):
    if not args[0] or (args[0][0] != "yes" and args[0][0] != "no"):
      raise RuntimeError("#3 Usage: /voteban <yes/no>")
    
    total_users = len(self.users)
    userAddr = args[1]
    if self.ban_target:
        voter_name = self.users[userAddr]
        if voter_name != self.ban_target and args[0][0] == "yes":
            if voter_name in self.ban_votes and self.ban_votes[voter_name] == True:
              raise RuntimeError("#1 You already vote yes")
            self.ban_votes[voter_name] = True
            # Enviar uma mensagem de voto para todos os usuários
            vote_count = sum(1 for vote in self.ban_votes.values() if vote)
            vote_message = "#0 [Server] {} voted YES to ban {}. {}/{} votes.".format(voter_name, self.ban_target, vote_count, total_users)
            if vote_count >= self.ban_threshold:
              for (addr, name) in self.users.items():
                if name == self.ban_target:
                  self.disconnectUser(addr)
                  vote_message += " User has been successfully banned!"
                  self.ban_target = None
                  break
            return vote_message
            
        elif voter_name != self.ban_target and args[0][0] == "no":
            if voter_name in self.ban_votes and self.ban_votes[voter_name] == False:
              raise RuntimeError("#1 You already vote no")
            self.ban_votes[voter_name] = False
            # Enviar uma mensagem de voto para todos os usuários
            vote_count = sum(1 for vote in self.ban_votes.values() if vote)
            vote_message = "#0 [Server] {} voted NO to ban {}. {}/{} votes.".format(voter_name, self.ban_target, vote_count, total_users)
            return vote_message
        else:
          raise RuntimeError("#1 You can't vote in our own ban.")
    else:
        raise RuntimeError("#1 No ban vote in progress.")
   

  def getMessage(self, *args):

    message = args[0]
    userAddr = args[1]

    if userAddr in self.users:
      # create objcts and append to others
      name = self.users[userAddr]
      newMessage = Message(User(name, userAddr[0], userAddr[1]), message)
      self.messages.append(newMessage)
      print('message received from ' + name + ': ' + message)
      return '#0 ' + newMessage.getString()
    else:
      print('Someone that is not logged in sent a message')
      raise RuntimeError("#1 You should log in before send messages, try: /hi <your_name>")

  def runCommand(self, command, text, retAddr):
    #if not logged you cannot execute a command
    if retAddr not in self.users and command != '/hi':
      raise RuntimeError("#1 You aren't logged-in, try login with: /hi <your_name>")

    #a command that does not exist
    elif command not in self.commands:
      print('Command does not exist')
      # return self.getMessage(text, retAddr) #if dont exist, it's a message!
      raise RuntimeError("#3 Did you try to type a command? that is the list you can use: {}".format(self.commands.keys()))

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
        return self.runCommand(words[0], words[1:] if len(words) > 1 else None, retAddr)

# instanciacao do server
server = Server('127.0.0.1', 6969)

print("Server running on port 6969. Waiting for messages...")
while True:
  # data, addr = socks.recvfrom(1024)
  # print(data.decode())
  with open('../server/tmpFile', 'w+b') as fd:
    ret_addr = server.rdt.rdt_recv(fd)
    fd.seek(0)
    message = fd.read().decode()

  try:
    messageBack = server.processCommand(message, ret_addr)
    for users in server.users: #broadcast send
      server.rdt.rdt_sendBytes(messageBack.encode(), users)
  except RuntimeError as e:
    server.rdt.rdt_sendBytes(str(e).encode(), ret_addr) #sending to just one client, that sent something wrong

