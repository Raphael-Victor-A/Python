#Servidor IP:127.0.0.1  Port:50000

import socket
import sys

HOST = '172.31.15.1'
PORT = 50000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv= (HOST,PORT)
print("serv on")
udp.bind((serv))
while True:
    msg, client = udp.recvfrom(1024)
    print(client,msg)
    udp.sendto(msg,client)
udp.close()
    