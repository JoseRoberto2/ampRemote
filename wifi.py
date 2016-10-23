# -*- coding: utf-8 -*-
__autor__="roberto"
import time
import socket
from Queue import Queue

entrada=Queue()

TCP_IP = '192.168.43.131'
TCP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = 0B00001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send(chr(MESSAGE))

while True:
    entrada2=str(input("verificar se o valor é par ou impar: "))
    if (entrada2=="sair"):
        break
    else:
        print entrada2
        s.send(entrada2)
    print("aguardando")
    data = s.recv(BUFFER_SIZE)
    time.sleep(1)
    s.send("chegou")
    temp = data.split()
    print temp
    entrada.put(temp[0])
    __temp=entrada.get()
    print __temp

s.close()

print "received data:", data