#Servidor TCP
import socket
import sys
host = 'localhost'
port = 50000 #porta do servidor
#criando o socket IPV4 TCP
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#lingando o socket na porta e no endereço IP
s.bind((host,port))
#O servidor fica escutando na porta 50000 no
#endereço ip 127.0.0.1
s.listen()
print('Aguardando conexões...')
conn,endr = s.accept()
print('Conectado a: ',endr)
#loop para ecoar os dados recebidos
while True:
    data=conn.recv(1024)
    print('dados recebidos: ',data.decode())
    if not data:
        print('Fechando a conexão!')
        conn.close()
        break
    conn.sendall(data)