#from csv import excel

__author__="Roberto"
#import thread
import threading


def funcaoP(nome, valor):
    int(valor)
    i = 0
    while i < valor:
        print (nome)
        print (i)
        i = i + 1

class threadClass(threading.Thread):
    def __init__(self,Nome,valor):
        threading.Thread.__init__(self)
        self.Nome=Nome
        self.valor=valor
    def run(self):
        print ("thead rodando")
        funcaoP(self.Nome,self.valor)



#def primeiraThread():
 #   str(name)
  #  i=0
   # while i<20:
    #    print "thead rodando"
     #   print i
      #  i=i+1
#try:
    #thread.start_new_thread(primeiraThread())
    #thread.start_new_thread(primeiraThread())
#except:
 #   print "nao rodou"

thr1=threadClass("primeira",10)
thread2=threadClass("segunda",10)

thr1.start()
thread2.start()

j=0
while j<0:
    print "jota"
    j=j+1