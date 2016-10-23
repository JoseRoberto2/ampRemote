from gi import require_version
from threading import Thread
import serial
import time
from Queue import Queue
import socket

require_version('Gtk', '3.0')
from gi.repository import Gtk


class Exec(object):
    input = 0B00000000
    volume = 0B00000010
    gainIn = 0B00000001
    bass = 0B00000100
    treble = 0B00000101
    atenuationR = 0B00000110
    atenuationL = 0B00000111

    matBass = [0B00000000, 0B00000001, 0B00000010, 0B00000011, 0B00000100, 0B00000101, 0B00000110, 0B00000111,
               0B00001110, 0B00001101, 0B00001100, 0B00001011, 0B00001010, 0B00001001, 0B00001000]

    matGainIn = [0B00000000, 0B00000001, 0B00000010, 0B00000011, 0B00000100, 0B00000101, 0B00000110, 0B00000111, 0B00001000,
                     0B00001001, 0B00001010, 0B00001011, 0B00001100, 0B00001101, 0B00001110, 0B00001111]

    matVol = [0B00000000, 0B00000001, 0B00000010, 0B00000011, 0B00000100, 0B00000101, 0B00000110, 0B00000111, 0B00001000,
                  0B00010000, 0B00011000, 0B00100000, 0B00101000, 0B00111000]

    matTreble = [0B00000000, 0B00000001, 0B00000010, 0B00000011, 0B00000100, 0B00000101, 0B00000110, 0B00000111, 0B00001110,
                     0B00001101, 0B00001100, 0B00001011, 0B00001010, 0B00001001, 0B00001000]

    matAtt = [0B00000000, 0B00000001, 0B00000010, 0B00000011, 0B00000100, 0B00000101, 0B00000110, 0B00000111, 0B00001000,
                  0B00010000, 0B00011000, 0B00100000, 0B00101000, 0B00110000, 0B00111000,0B01000000,0B01001000,0B0111000]

    matInput = [0B00000010, 0B00000011]
    flagSerial = True

    def __init__(self, builder, queue_entrada, queue_saida):


        self.queue_entrada = queue_entrada
        self.queue_saida = queue_saida

        # Telas
        self.window = builder.get_object("window2")

        self.window.show()

        # Widgets
        self.barraLow = builder.get_object('escale_low')
        self.barraTreble = builder.get_object('escale_treble')
        self.barraVolume = builder.get_object('escale_volume')
        self.barraGain = builder.get_object('escale_gain')
        self.barraAttR = builder.get_object('escale_AttR')
        self.barraAttL = builder.get_object('escale_AttL')
        self.botaoinput1=builder.get_object('in1')
        self.botaoinput2=builder.get_object('in2')

        self.porta = builder.get_object('txt_porta')



        #self.barraLow.range()

        # Signals
        builder.connect_signals({
            "on_main_destroy": self.on_destroy,
            "on_button2_clicked":self.actionButton,
            "on_cx_button_press_event": self.on_button_toggled,
            "on_escale_low_value_changed":self.scaleLow,
            "on_escale_treble_value_changed":self.scaleTreble,
            "on_escale_volume_value_changed":self.scaleVol,
            "on_escale_gain_value_changed": self.scaleGain,
            "on_escale_AttR_value_changed": self.scaleAttR,
            "on_escale_AttL_value_changed": self.scaleAttL,
            "on_conection_activate":self.conectar
        })




    def conectar(self,widget):
        #self.Comunicacao = serial.Serial(str(self.porta.get_text()), 9600)
        #if self.Comunicacao.isOpen():
        print('conectou')
        #thread.start_new_thread(target=Exec.RxSerial(), args=(str(self.porta.get_text())))
        #Thread(target=self.RxSerial()).start()
        #worker = Thread(target=self.RxSerial())
        #worker.setDaemon(True)
        #worker.run()
        #worker.start()
        #leitura = leituraSerial(str(self.porta.get_text()))
        #leitura.start()
        ##vai=ComSerial(str(self.porta.get_text()),queue_entrada,queue_saida)
        #vai.start()
        sok=initSocket(str(self.porta.get_text()),queue_entrada,queue_saida)
        sok.start()
        atualiza=atualizaValores(self.barraVolume,self.barraGain,self.barraLow,self.barraTreble,self.barraAttR,self.barraAttL,queue_entrada)
        atualiza.start()

    def actionButton(self,event):
        print("vc clicou no botao")


    def scaleLow(self, widget):
        posicao=14-int(self.barraLow.get_value())
        #low = enviarSerial(self.bass,self.matBass[posicao],posicao,str(self.porta.get_text()))
        #low.start()
        queue_saida.put(self.bass)
        queue_saida.put(self.matBass[posicao])
        queue_saida.put(posicao)
        print"low"


    def scaleTreble(self,widget):
        posicao = 14-int(self.barraTreble.get_value())
        #treble = enviarSerial(self.treble, self.matTreble[posicao],posicao, str(self.porta.get_text()))
        #treble.start()
        queue_saida.put(self.treble)
        queue_saida.put(self.matTreble[posicao])
        queue_saida.put(posicao)
        print"treble"

    def scaleVol(self, widget):
        #self.Comunicacao = serial.Serial('/dev/ttyACM1', 9600)
        posicao = 13-(int(self.barraVolume.get_value()))
        #time.sleep(1.8)
        #vol = enviarSerial(self.volume, posicao, self.Comunicacao)
        #print posicao
        #imprimir=chr(0B10)
        #imprimir2=chr(13-posicao)
        #self.Comunicacao.write(imprimir)
        #time.sleep(1)
        #self.Comunicacao.write(imprimir2)
       # self.Comunicacao.write('/n')

        #self.Comunicacao.close()

        #vol = enviarSerial(self.volume, self.matVol[posicao], posicao, str(self.porta.get_text()))
        #vol.start()
        #threads.append(vol)
        queue_saida.put(self.volume)
        queue_saida.put(self.matVol[posicao])
        queue_saida.put(posicao)
        print"vol"

    def scaleGain(self, widget):
        posicao = (int(self.barraGain.get_value()))
        print posicao

        #gain = enviarSerial(self.gainIn, self.matGainIn[posicao],posicao, str(self.porta.get_text()))
        #gain.start()
        queue_saida.put(self.gainIn)
        queue_saida.put(self.matGainIn[posicao])
        queue_saida.put(posicao)
        print"gain"

    def scaleAttR(self, widget):
        posicao = (int(self.barraAttR.get_value()))
        print posicao

        #attR = enviarSerial(self.atenuationR, self.matAtt[posicao],posicao, str(self.porta.get_text()))
        #attR.start()
        queue_saida.put(self.atenuationR)
        queue_saida.put(self.matAtt[posicao])
        queue_saida.put(posicao)
        print"attr"


    def scaleAttL(self, widget):
        posicao = (int(self.barraAttL.get_value()))
        print posicao

        #attL = enviarSerial(self.atenuationL, self.matAtt[posicao],posicao, str(self.porta.get_text()))
        #attL.start()
        queue_saida.put(self.atenuationL)
        queue_saida.put(self.matAtt[posicao])
        queue_saida.put(posicao)
        print"attl"


    def on_destroy(self, widget):
        queue_saida.put('sair')
        queue_entrada.put('sair')
        #self.Comunicacao.close()

        Gtk.main_quit()

        print("aki")



    def on_button_toggled(self,widget):
        print("botao selecionado")
        if self.botaoinput1.get_active():
            print("botao1")

        else:
            print("botao2")


class ComSerial(Thread):
    def __init__(self,porta, queue_entrada,queue_saida):
        Thread.__init__(self)
        self.porta=porta
        self.queue_entrada = queue_entrada
        self.queue_saida= queue_saida
    def run(self):
        #self.Com = serial.Serial(self.porta, 9600)
        while True:
            self.Com = serial.Serial(self.porta, 9600)

            print "atualizando"
            # self.Com.flush()
            testeRx=self.Com.readline()
            #testeRx=bytes(testeRx)
            if (testeRx=='255\r\n'):
                i = 0
                while i <= 6:
                    temp=self.Com.readline()
                    if (temp!='255\r\n'):
                        'passou'
                        queue_entrada.put(temp)
                        print temp
                        i += 1

            if(not queue_saida.empty()):
                print("enviando")
                A=queue_saida.get()
                if (A=='sair'):
                    break
                B = queue_saida.get()
                C = queue_saida.get()
                self.Com.write(chr(A))
                self.Com.write(chr(B))
                self.Com.write(chr(C))
                print A,B,C


            self.Com.close()
        print "saiu"


class initSocket(Thread):
    def __init__(self, ip, queue_entrada, queue_saida):
        Thread.__init__(self)
        #super(initSocket, self).__init__()
        self.__que_ent = queue_entrada
        self.__que_sai = queue_saida
        self.__ip = ip
        self.__port = 4000
        self.__buffer = 1024

    def run(self):
        print "iniciado socket"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.__ip, self.__port))
        while True:
            print "esperando dado"
            __dataIn=s.recv(self.__buffer)
            print"chegou dado"
            print __dataIn
            time.sleep(1)
            convData=__dataIn.split()
            for a in convData:
                self.__que_ent.put(a)


        s.close()

class atualizaValores(Thread):
    def __init__(self, sca1,sca2,sca3,sca4,sca5,sca6,queue_entrada):
        Thread.__init__(self)
        self.sca1 = sca1
        self.sca2 = sca2
        self.sca3 = sca3
        self.sca4 = sca4
        self.sca5 = sca5
        self.sca6 = sca6
        self.queue_entrada = queue_entrada


    def run(self):
        #self.sca1.set_value(4)
        #self.sca2.set_value(4)
        #self.sca3.set_value(4)
        #print "entrou"
        while True:
            if (not queue_entrada.empty()):
                A = queue_entrada.get()
                #if (A=='sair'):
                #    break
                B = queue_entrada.get()
                C = queue_entrada.get()
                D = queue_entrada.get()
                E = queue_entrada.get()
                F = queue_entrada.get()
                G = queue_entrada.get()
                self.sca1.set_value(int(A))
                self.sca2.set_value(int(B))
                self.sca3.set_value(int(C))
                self.sca4.set_value(int(D))
                self.sca5.set_value(int(E))
                self.sca6.set_value(int(F))
                self.inputAud = G


if __name__ == "__main__":

    queue_entrada = Queue()
    queue_saida = Queue()

    builder = Gtk.Builder()
    builder.add_from_file("ideAmp.glade")
    browser = Exec(builder, queue_entrada=queue_entrada, queue_saida=queue_saida)

    Gtk.main()
    #queue_entrada.join()
    #queue_saida.join()
    #Exec.ComSerial=False