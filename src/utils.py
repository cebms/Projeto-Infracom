import socket as sck


class UDP:

  def __init__(self, addr=None):
    self.socks = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    if addr != None:
      self.socks.bind(addr)

  def recv_data(self):
    data, addr = self.socks.recvfrom(1024)
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
    self.TIMEOUT_INTERVAL = 10  #time in seconds
    self.udp = UDP(addr)

  def isId(self, rcvpkt, ack):
    return (rcvpkt[0] % 2 == ack)

  def isEOF(self, rcvpkt):
    return rcvpkt[0] >= 2

  def rdt_send(self, file_name, addr):
    latest_packet = bytes()
    with open(file_name, 'rb') as file:
      while True:
        if self.stateSend == 0 or self.stateSend == 2:
          print('Transmissor state: ' + str(self.stateSend))
          #create packet (if remaining data)
          data = file.read(1023)
          latest_packet = data
          #send packet
          id = 0 if self.stateSend == 0 else 1
          self.udp.send_data(data, id, addr, eof=0 if len(data) else 1)
          #start timer
          self.udp.start_timer(self.TIMEOUT_INTERVAL)
          self.stateSend += 1

        else:
          #if timeout, send again and restart timer
          id = 0 if self.stateSend == 1 else 1
          #if received ack, but not the one expected, ignore
          print('Transmissor state: ' + str(self.stateSend))
          try:
            #espera o ack
            recvpkt, ret_addr = self.udp.recv_data()
            if self.isId(recvpkt, id):
              print('ACK ' + str(id) + ' recebido')
              self.stateSend = (self.stateSend + 1) % 4  # 1 -> 2, 3 -> 0
              if not len(latest_packet):  #end of file
                break
          except sck.timeout:
            #envia o pacote de novo
            self.udp.send_data(latest_packet, id, addr)
            print('Retransmitindo ' + str(id))
            self.udp.start_timer(self.TIMEOUT_INTERVAL)
          #if received ack, and is the one expected, stop timer and go to stateSend 2

  def rdt_recv(self, destination):
    WAIT0 = 0
    WAIT1 = 1
    while True:
      rcvpkt, ret_addr = self.udp.recv_data()
      if self.stateRecv == WAIT0:
        if self.isId(rcvpkt, 0):
          print("pacote 0 recebido")
          destination.write(rcvpkt[1:])
          self.udp.send_data(bytes(), seq_num=0, addr=ret_addr)
          self.stateRecv = WAIT1
        else:
          self.udp.send_data(bytes(), seq_num=1, addr=ret_addr)
      elif self.stateRecv == WAIT1:
        if self.isId(rcvpkt, 1):
          print("pacote 1 recebido")
          destination.write(rcvpkt[1:])
          self.udp.send_data(bytes(), seq_num=1, addr=ret_addr)
          self.stateRecv = WAIT0
        else:
          self.udp.send_data(bytes(), seq_num=0, addr=ret_addr)

      if self.isEOF(rcvpkt):
        break
