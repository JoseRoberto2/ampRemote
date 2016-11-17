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
    flagRecebe = True

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
        print('CONECTANDO')
        sok=initSocket(str(self.porta.get_text()),queue_entrada,queue_saida)
        sok.start()
        atualiza=atualizaValores(self.barraVolume,self.barraGain,self.barraLow,self.barraTreble,self.barraAttR,self.barraAttL,queue_entrada)
        atualiza.start()

    #def actionButton(self,event):
        #print("vc clicou no botao")


    def scaleLow(self, widget):
        posicao=int(self.barraLow.get_value())
        queue_saida.put(str(self.bass))
        queue_saida.put(str(self.matBass[posicao]))
        queue_saida.put(str(posicao))
        print"low"


    def scaleTreble(self,widget):
        posicao = int(self.barraTreble.get_value())
        queue_saida.put(str(self.treble))
        queue_saida.put(str(self.matTreble[posicao]))
        queue_saida.put(str(posicao))
        print"treble"

    def scaleVol(self, widget):
        posicao = (int(self.barraVolume.get_value()))
        queue_saida.put(str(self.volume))
        queue_saida.put(str(self.matVol[posicao]))
        queue_saida.put(str(posicao))
        print"vol"

    def scaleGain(self, widget):
        posicao = (int(self.barraGain.get_value()))
        queue_saida.put(str(self.gainIn))
        queue_saida.put(str(self.matGainIn[posicao]))
        queue_saida.put(str(posicao))
        print"gain"

    def scaleAttR(self, widget):
        posicao = (int(self.barraAttR.get_value()))
        queue_saida.put(str(self.atenuationR))
        queue_saida.put(str(self.matAtt[posicao]))
        queue_saida.put(str(posicao))
        print"attr"


    def scaleAttL(self, widget):
        posicao = (int(self.barraAttL.get_value()))
        queue_saida.put(str(self.atenuationL))
        queue_saida.put(str(self.matAtt[posicao]))
        queue_saida.put(str(posicao))
        print"attl"


    def on_destroy(self, widget):
        queue_saida.put('sair')
        queue_entrada.put('sair')
        Exec.flagRecebe=False
        #self.Comunicacao.close()

        Gtk.main_quit()

        print("FINALIZADO")



    #def on_button_toggled(self,widget):
        #print("botao selecionado")
        #if self.botaoinput1.get_active():
        #    print("botao1")

        #else:
        #    print("botao2")


class initSocket(Thread):
    def __init__(self, ip, queue_entrada, queue_saida):
        Thread.__init__(self)
        #super(initSocket, self).__init__()
        self.__que_ent = queue_entrada
        self.__que_sai = queue_saida
        self.__ip = ip
        self.__port = 4000

    def run(self):
        print "iniciado socket"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.__ip, self.__port))
        recebe=recebeValores(conexao=s,queue_entrada=queue_entrada)
        recebe.start()

        while True:
            flagSend=False
            # envia dado para o mcu
            if not queue_saida.empty():
                flagSend=True
                print "enviando"
                A = queue_saida.get() + "_"
                if A == "sair_":
                    break
                B = queue_saida.get() + "_"
                C = queue_saida.get() + "_"
                Tx='2'+','+'_16'+','+'_7'+','
                #s.send(Tx)
                s.send(A)
                time.sleep(1)
                s.send(B)
                time.sleep(1)
                s.send(C)
                time.sleep(1)

                print A, B, C
        print("saiu")
        s.close()

class recebeValores(Thread):
    def __init__(self,conexao,queue_entrada):
        Thread.__init__(self)
        self.conexao=conexao
        self.queue_ent=queue_entrada
        self.__buffer = 18

    def run(self):
        # recebe dado do mcu
        while True:

            if Exec.flagRecebe == False:
                print 'saiu recebe'
                break
            print "esperando dado"
            #time.sleep(3)
            __dataIn = self.conexao.recv(self.__buffer)
            print"chegou dado"
            print __dataIn
            convData = __dataIn.split()
            for a in convData:
                self.queue_ent.put(a)



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
        while True:
            if (not queue_entrada.empty()):
                A = queue_entrada.get()
                if (A=='sair'):
                    break
                B = queue_entrada.get()
                C = queue_entrada.get()
                D = queue_entrada.get()
                E = queue_entrada.get()
                F = queue_entrada.get()
                #G = queue_entrada.get()
                time.sleep(1.2)
                self.sca1.set_value(int(A))
                self.sca2.set_value(int(B))
                self.sca3.set_value(int(C))
                self.sca4.set_value(int(D))
                self.sca5.set_value(int(E))
                self.sca6.set_value(int(F))
                #self.inputAud = G


if __name__ == "__main__":

    queue_entrada = Queue()
    queue_saida = Queue()

    builder = Gtk.Builder()
    builder.add_from_file("ideAmp.glade")
    browser = Exec(builder, queue_entrada=queue_entrada, queue_saida=queue_saida)

    Gtk.main()