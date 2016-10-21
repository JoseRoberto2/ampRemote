import Tkinter
import serial
import threading


class leituraSerial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #self.porta = porta
        self.Comunicacao = serial.Serial('/dev/ttyACM1',9600)

    def run(self):
        i = 0
        while i < 30:

            j = self.Comunicacao.read()
            print(j)
            i+=1
        self.Comunicacao.close()

thta1 = leituraSerial()
thta1.start()
