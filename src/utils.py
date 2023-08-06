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