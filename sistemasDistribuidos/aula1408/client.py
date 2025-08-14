import socket
import sys

HOST = '172.31.15.1'
PORT = 50000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest= (HOST,PORT)
print("para sair use CTRL+C\n")
msg = str.encode("0")
while msg != '\x18':
    msg = input()
    msg2 = str.encode(msg)
    udp.sendto(msg2,dest)
    msg3,serv = udp.recv(1024)
    print(serv,msg3)
udp.close()