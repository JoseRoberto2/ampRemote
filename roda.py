from gi import require_version
from threading import Thread
import serial
import time
from Queue import Queue

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
        self.Comunicacao=""


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
        atualiza=atualizaValores(self.barraVolume,self.barraGain,self.barraLow,self.barraTreble,self.atenuationR,self.atenuationL,queue_entrada)
        atualiza.start()

    def actionButton(self,event):
        print("vc clicou no botao")


    def scaleLow(self, widget):
        posicao=14-int(self.barraLow.get_value())
        low = enviarSerial(self.bass,self.matBass[posicao],posicao,str(self.porta.get_text()))
        low.start()


    def scaleTreble(self,widget):
        posicao = 14-int(self.barraTreble.get_value())
        treble = enviarSerial(self.treble, self.matTreble[posicao],posicao, str(self.porta.get_text()))
        treble.start()

    def scaleVol(self, widget):
        #self.Comunicacao = serial.Serial('/dev/ttyACM1', 9600)
        posicao = 13-(int(self.barraVolume.get_value()))
        #time.sleep(1.8)
        #vol = enviarSerial(self.volume, posicao, self.Comunicacao)
        print posicao
        #imprimir=chr(0B10)
        #imprimir2=chr(13-posicao)
        #self.Comunicacao.write(imprimir)
        #time.sleep(1)
        #self.Comunicacao.write(imprimir2)
       # self.Comunicacao.write('/n')

        #self.Comunicacao.close()

        vol = enviarSerial(self.volume, self.matVol[posicao], posicao, str(self.porta.get_text()))
        vol.start()
        #threads.append(vol)

    def scaleGain(self, widget):
        posicao = (int(self.barraGain.get_value()))
        print posicao

        gain = enviarSerial(self.gainIn, self.matGainIn[posicao],posicao, str(self.porta.get_text()))
        gain.start()

    def scaleAttR(self, widget):
        posicao = (int(self.barraAttR.get_value()))
        print posicao

        attR = enviarSerial(self.atenuationR, self.matAtt[posicao],posicao, str(self.porta.get_text()))
        attR.start()


    def scaleAttL(self, widget):
        posicao = (int(self.barraAttL.get_value()))
        print posicao

        attL = enviarSerial(self.atenuationL, self.matAtt[posicao],posicao, str(self.porta.get_text()))
        attL.start()


    def on_destroy(self, widget):
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


    def RxSerial(self):
        #porta=porta
        #Comuni = serial.Serial(porta, 9600)
        #while Exec.ComSerial:
        while(True):
        #for i in range(0,50):
            #memoria = Comuni.read()
            #print(memoria)
            #value = Comuni.read()
            #print(value)
             print(str(self.porta.get_text()))
             #time.sleep(1)

class enviarSerial(Thread):
    def __init__(self,memori,valor,posicao,porta, queue_entrada):
        Thread.__init__(self)
        self.memori=chr(memori)
        self.valor=chr(valor)
        self.porta=porta
        self.posicao=chr(posicao)
    def run(self):
        #threadLock.acquire()
        print(self.memori,self.valor,self.posicao)
        self.Com = serial.Serial(self.porta, 9600)
        #print(serial.tools.list_port)
        self.Com.write(self.memori)
        self.Com.write(self.valor)
        self.Com.write(self.posicao)
        self.Com.close()
        #threadLock.release()

class leituraSerial(Thread):
    def __init__(self,porta):
        Thread.__init__(self)
        self.porta=porta
        self.Comuni = serial.Serial(self.porta,9600)

    def run(self):
        while Exec.ComSerial:

            self.memoria = self.Comuni.read()
            print(self.memoria)

            value = self.Comuni.read()
            print(self.memoria)

            print Exec.ComSerial
            #print(Exec.barraVolume.get_value())
            #muda =Exec
            #muda.barraVolume.set_value(5)
            #if (self.memoria==Exec.bass):
            #    Exec.barraLow.set_value(self.value)

            #elif(self.memoria==Exec.treble):
            #    Exec.barraTreble.set_value(self.value)

            if (self.memoria == 2):
                muda=Exec
                muda.pot()
        print("saiu")
        self.Comunicacao.close()



class atualizaValores(Thread):
    def __init__(self, sca1,sca2,sca3,sca4,sca5,sca6,queue_entrada):
        Thread.__init__(self)
        self.sca1 = sca1
        self.sca2 = sca2
        self.sca3 = sca3
        self.sca4 = sca4
        self.sca5 = sca5
        self.sca6 = sca6
        self.queue_entrada=queue_entrada


    def run(self):
        self.sca1.set_value(4)
        self.sca2.set_value(4)
        self.sca3.set_value(4)
        while True:
            print "funcio"

            if (not queue_entrada.empty()):
                queue_entrada.get()
                if (queue_entrada.get()=='sair'):
                    break


#threadLock = threading.Lock()
#threads = []

if __name__ == "__main__":

    queue_entrada = Queue()
    queue_saida = Queue()

    builder = Gtk.Builder()
    builder.add_from_file("ideAmp.glade")
    browser = Exec(builder, queue_entrada=queue_entrada, queue_saida=queue_saida)



    Gtk.main()

    #Exec.ComSerial=False