#Cliente TCP
import socket
import sys

host ='localhost' #endereço do servido
port = 50000     #porta onde o servidor está
            #aguardando a conexão
#Criando o socket IPV4 TCP
c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Com o servidor criado vamos pedir uma conexão com o servidor
c.connect((host,port))
#Após conectar no servidor vamos enviar os dados
msg=''
while msg !='\x18':
    msg=input()
    msg2 = str.encode(msg)
    #enviando os dados...
    c.sendall(msg2)
    #após enviar os dados aguardar a resposta
    #do servidor. Se tudo ocorrer como esperado
    #a mensagem será ecoada
    data=c.recv(1024)
    print('Mensagem ecoada: ',data.decode())
c.close()