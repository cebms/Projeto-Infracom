import socket as sck

MESSAGE = b'hello ma bro'
UDDP_IP = '127.0.0.1'
PORT = 6969

my_socks = sck.socket(sck.AF_INET,
                      sck.SOCK_DGRAM)

file = open('file.txt', 'rb')
#print(len(data))
while(1):
    data = file.read(1024)
    if len(data) == 0:
        break
    my_socks.sendto(data, (UDDP_IP, PORT))
#    print(i, c)
file.close()


