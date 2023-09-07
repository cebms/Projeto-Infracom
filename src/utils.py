import socket as sck

class UDP:

  def __init__(self):
    self.socks = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    
  def recv_file(self):
    data_total = bytes()
    addr = None
    while 1:
      self.socks.settimeout(3)
      try:
        data, addr = self.socks.recvfrom(1024)
        print(addr)
        data_total += data
      except sck.timeout:
        return data_total, addr

  def send_file(self, file_name, addr):
    with open(file_name, 'rb') as file:
      while (1):
        data = file.read(1024)
        if len(data) == 0:
          break
        self.socks.sendto(data, addr)

class rdt3_sender:
    def __init__(self):
        self.state = 0 #waiting for call 0
        self.socks = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

    def rdt_send(self, file_name, addr):
        with open(file_name, 'rb') as file:
            while True:
                if self.state == 0:
                    #create packet (if remaining data)
                    data = file.read(1023)
                    
                    #send packet
                    #start timer
                    self.state = 1
                    pass
                elif self.state == 1:
                    #if timeout, send again and restart timer
                    #if received ack, but not the one expected, ignore
                    #if received ack, and is the one expected, stop timer and go to state 2
                    pass
                elif self.state == 2:
                    #create packet (if remaining data)
                    #send packet
                    #start timer
                    self.state = 3
                    pass
                elif self.state == 3:
                    #if timeout, send again and restart timer
                    #if received ack, but not the one expected, ignore
                    #if received ack, and is the one expected, stop timer and go to state 0
                    pass