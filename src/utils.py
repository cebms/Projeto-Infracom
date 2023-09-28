import socket as sck
import random as rnd
import datetime
import copy
import io

class UDP:

  def __init__(self, addr=None):
    self.socks = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    if addr != None:
      self.socks.bind(addr)

  def recv_data(self, recv_prob=1.0):
    random = 1.0
    while random >= recv_prob:  #simulating packet miss
      data, addr = self.socks.recvfrom(1024)
      random = rnd.random()
    return data, addr

  def send_data(self, data, seq_num, addr, eof=0):
    packet = bytes()
    seq_num = seq_num + 2 if eof else seq_num  #seq_num + 2 to set the second bit as 1, end of file
    pckt_header = seq_num.to_bytes(1, 'big')
    packet = pckt_header + data
    self.socks.sendto(packet, addr)

  def start_timer(self, time):
    self.socks.settimeout(time)


class Rdt3:

  def __init__(self, addr=None):
    self.stateSend = 0  #waiting for call 0
    self.stateRecv = 0
    self.TIMEOUT_INTERVAL = 0.5  #time in seconds
    self.udp = UDP(addr)

  def isId(self, rcvpkt, id):
    return (rcvpkt[0] % 2 == id)

  def isEOF(self, rcvpkt):
    return rcvpkt[0] >= 2

  def rdt_send(self, file_name, addr):
    with open(file_name, 'rb') as file:
      self.rdt_sendBytes(file, addr)

  def rdt_sendBytes(self, bytesToSend, addr):
    # if we receive bytes we must transform it to a bufferedIOBytes, to use read method, if it's a file, no changes
    bytesToSend = io.BytesIO(bytesToSend) if type(bytesToSend) == bytes else bytesToSend

    latest_packet = bytes()
    self.stateSend = 0
    ret_count = 0
    while True:
      if self.stateSend == 0 or self.stateSend == 2:
        #print('Transmissor state: ' + str(self.stateSend))
        #create packet (if remaining data)
        data = bytesToSend.read(1023)
        latest_packet = data
        #send packet
        id = 0 if self.stateSend == 0 else 1
        #print('Enviando pacote ' + str(id))

        self.udp.send_data(data, id, addr, eof=0 if len(data) else 1)
        #start timer
        self.udp.start_timer(self.TIMEOUT_INTERVAL)
        self.stateSend += 1
        ret_count = 0

      else:
        #if timeout, send again and restart timer
        id = 0 if self.stateSend == 1 else 1
        #if received ack, but not the one expected, ignore
        #print('Transmissor state: ' + str(self.stateSend))
        try:
          #espera o ack
          recvpkt, ret_addr = self.udp.recv_data()
          if self.isId(recvpkt, id):
            #print('ACK ' + str(id) + ' recebido')
            self.stateSend = (self.stateSend + 1) % 4  # 1 -> 2, 3 -> 0
            if not len(latest_packet):  #end of file
              self.udp.start_timer(None)
              return True
        except sck.timeout:
          #envia o pacote de novo
          if ret_count > 5:  #ultimo ack perdido
            #print('Muitas retransmissoes, encerrando conexao!')
            self.udp.start_timer(None)
            return False
          self.udp.send_data(latest_packet,
                              id,
                              addr,
                              eof=0 if len(latest_packet) else 1)
          #print('Temporizador estorou!\nRetransmitindo ' + str(id))
          self.udp.start_timer(self.TIMEOUT_INTERVAL)
          ret_count += 1
        #if received ack, and is the one expected, stop timer and go to stateSend 2

  def rdt_recv(self, destination, waitTime = None):
    WAIT0 = 0
    WAIT1 = 1
    self.stateRecv = WAIT0
    while True:
      self.udp.start_timer(waitTime)
      rcvpkt, ret_addr = self.udp.recv_data()

      if self.stateRecv == WAIT0:
        #print('Receiver state: ' + str(self.stateRecv))
        if self.isId(rcvpkt, 0):
          #print("pacote 0 recebido\nACK 0 enviado")
          destination.write(rcvpkt[1:])
          self.udp.send_data(bytes(), seq_num=0, addr=ret_addr)
          self.stateRecv = WAIT1
        else:
          self.udp.send_data(bytes(), seq_num=1, addr=ret_addr)
          #print('ACK 1 enviado')
      elif self.stateRecv == WAIT1:
        #print('Receiver state: ' + str(self.stateRecv))
        if self.isId(rcvpkt, 1):
          #print("pacote 1 recebido\nACK 1 enviado")
          destination.write(rcvpkt[1:])
          self.udp.send_data(bytes(), seq_num=1, addr=ret_addr)
          self.stateRecv = WAIT0
        else:
          self.udp.send_data(bytes(), seq_num=0, addr=ret_addr)
          #print('ACK 0 enviado')

      if self.isEOF(rcvpkt):
        return ret_addr
        break

class User:

  def __init__(self, name, IP, port):
    self.IP = IP
    self.port = port
    self.name = name
    self.friends = []

  def addFriend(self, user):
    self.friends.append(copy.deepcopy(user))

  def removeFriend(self, user):
    friends_copy = self.friends[:]
    for classUser in friends_copy:
      if user.name == classUser.name:
        self.friends.remove(classUser)


class Message:

  def __init__(self, user, text=""):
    self.user = user
    self.text = text
    self.time = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")

  def show(self):
    print(self.user.IP + ':' + str(self.user.port) + '/~' + self.user.name +
          ': ' + self.text + ' ' + self.time)

  def getString(self):
    return (green(self.user.IP + ':' + str(self.user.port)+ '/')  + blue('~' + self.user.name) +
          ': ' + self.text + ' ' + gray(self.time))


# Para printar a messagem em vermelho
def red(texto):
  return "\033[91m" + texto + "\033[0m"

# Para printar a messagem em verde
def green(texto):
  return "\033[92m" + texto + "\033[0m"

# Para printar a messagem em amarelo
def yellow(texto):
  return "\033[93m" + texto + "\033[0m"

# To print the message in blue
def blue(texto):
  return "\033[94m" + texto + "\033[0m"

# To print the message in gray
def gray(texto):
  return "\033[90m" + texto + "\033[0m"
