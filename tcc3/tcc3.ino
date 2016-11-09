#include <Wire.h>
#include <LiquidCrystal.h>

/*
 =================================
LCD pin              Connect to
 ---------------------------------
 01 - GND             GND, pot     (verde)
 02 - VCC             +5V, pot     (laranja)
 03 - Contrast        GND
 04 - RS              Pin8 (P2_0)  (branco_verde
 05 - R/W             GND
 06 - EN              Pin9 (P2_6)  (branco_laranja)
 07 - DB0             GNDvubj                                                                                               
 
 08 - DB1             GND
 09 - DB2             GND
 10 - DB3             GND
 11 - DB4             Pin10 (P4_3) (marrom)
 12 - DB5             Pin11 (P4_0) (marrom)
 13 - DB6             Pin12 (P3_7) (marrom)
 14 - DB7             Pin13 (P1_2) (marrom)
 15 - BL+             +5V
 16 - BL-             GND
 =================================
*/

#define timeTX 2000

byte matGainIn[16] = {B00000000, B00000001, B00000010, B00000011, B00000100, B00000101, B00000110, B00000111, B00001000, B00001001, B00001010, B00001011, B00001100, B00001101, B00001110, B00001111};
byte matVol[14] = {B00000000, B00000001, B00000010, B00000011, B00000100, B00000101, B00000110, B00000111, B00001000, B00010000, B00011000, B00100000, B00101000, B00111000};
byte matBass[15] = {B00000000, B00000001, B00000010, B00000011, B00000100, B00000101, B00000110, B00000111, B00001110, B00001101, B00001100, B00001011, B00001010, B00001001, B00001000};
byte matTreble[15] = {B00000000, B00000001, B00000010, B00000011, B00000100, B00000101, B00000110, B00000111, B00001110, B00001101, B00001100, B00001011, B00001010, B00001001, B00001000};
byte matAtt[18] = {B00000000, B00000001, B00000010, B00000011, B00000100, B00000101, B00000110, B00000111, B00001000, B00010000, B00011000, B00100000, B00101000, B00110000, B00111000,B01000000,B01001000,B0111000};
byte matInput[2] = {B00000010, B00000011};

int maxMin[7]={13,15,14,14,17,17,1}; //vol,GainIn,Bass,Treble,AttR,AttL,Input
int ValueState[7]={07,00,07,07,01,01,00}; //vol,GainIn,Bass,Treble,AttR,AttL,Input
const byte functionSelect[7]={B00000010,B00000001,B00000100,B00000101,B00000110,B00000111,B00000000}; //vol,GainIn,Bass,Treble,AttR,AttL,Input


//uint8_t adress = B1000100;
byte adress = B01000100 ;
//byte input = B00000000;
//byte volume = B00000010; //B=0 endereço do volume
//byte gainIn = B00000001; //ganho de entrada
//byte bass = B00000100; // ganho do grave
//byte treble = B00000101; //ganho do agudo
//byte atenuationR = B00000110; //endereço da atenação da saida R
//byte atenuationL = B00000111; //endereço da atenuação da saida L

const int menu = P2_5;
const int cima = P2_4;
const int baixo = P1_5;
const int A=P8_1;
const int B=P8_2;


int stateMenu = 0;
//int stateVol = 7;
//int stateGainIn = 0;
//int stateBass = 8;
//int stateTreble = 8;
//int stateAttR = 1;
//int stateAttL = 1;
//int stateInput = 0;
int valorEnc=0;
int anterior = 1;
int lerA;
boolean flagSend=false;
boolean stateTemp=0;
int contEnt=0;
char comp1[10]="+IPD,0,8:";

//variaveis do Rxwifi
int tamanho=0;
int RxByte[3];
char leitura;
String RxWIFI;
boolean valida;
int i=0;
int in;


byte memori;
byte value;
char RxSerial[3];
String ValoresLCD;
byte flagChegou=0;

int timeTxcurent=0;

LiquidCrystal lcd(P2_0, P2_6, P4_3, P4_0, P3_7, P1_2);


void setup() {
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  //pinMode(P1_4,OUTPUT);
  Wire.begin();
  Serial.begin(9600);
  Serial1.begin(9600);

  pinMode(menu, INPUT_PULLUP);
  //pinMode(A,INPUT_PULLUP);
  //pinMode(B,INPUT_PULLUP);
  lcd.begin(16,2);
 
 //attachInterrupt(A,encodeR,CHANGE);
 
  lcd.setCursor(0,0);
  lcd.print("iniciando EQU!!!");
  inic();
  lcd.setCursor(0,0);
  lcd.print("iniciando WIFI!!");
  WifiTCPinit();
  //enviaWIFI();
  lcd.clear();
  //digitalWrite(P1_4,LOW);
}

void loop() {




  if(digitalRead(baixo)==LOW){
    stateTemp=false;
    flagSend=true;
    delay(300);
  }
  if(digitalRead(cima)==LOW){
    stateTemp=true;
    flagSend=true;
    delay(300);
  }

  if (digitalRead(menu) == LOW) {
    //digitalWrite(RED_LED,HIGH);
    if (stateMenu != 6)
      stateMenu++;
    else
      stateMenu = 0;
    //Serial.print("menu");
    //Serial.println(stateMenu);
    delay(500);
  }

  
//enviar quando acionado os butoes
  if(flagSend){
  
    memori=functionSelect[stateMenu];
    
     if (ValueState[stateMenu] != maxMin[stateMenu] && stateTemp==true)
            ValueState[stateMenu]=ValueState[stateMenu]+1;
     if (ValueState[stateMenu] != 0 && stateTemp==false)
            ValueState[stateMenu]=ValueState[stateMenu]-1;
     
     
     switch (stateMenu){
        case 0:
          value = matVol[ValueState[stateMenu]];
          break;
  
        //GainIn
        case 1:
          value = matGainIn[ValueState[stateMenu]];
          break;
  
        //Bass
        case 2:
          value=matBass[ValueState[stateMenu]];
          break;
  
        //Treble
        case 3:
          value=matTreble[ValueState[stateMenu]];
          break;
  
        //Atenuation Right
        case 4:
          value=matAtt[ValueState[stateMenu]];
          break;
  
        //Atenuation Left
        case 5:
          value=matAtt[ValueState[stateMenu]];
          break;
  
        //Input
        case 6:
          value=matInput[ValueState[stateMenu]];
          break;
        default:;
      };
  
    envairi2c(memori,value);
    flagSend=false;
    enviaWIFI();
  }
  //lcd.clear();

  switch (stateMenu){
        case 0:
          lcd.setCursor(0,0);
          lcd.print("VOLUME          ");
          if(ValueState[0]>9)
            lcd.setCursor(2,1);
          else{
            lcd.setCursor(2,1);
            lcd.print("0");
            lcd.setCursor(3,1);
          }
          lcd.print(ValueState[0]);
          break;
  
        //GainIn
        case 1:
          lcd.setCursor(0,0);
          lcd.print("GAIN INPUT      ");
          if(ValueState[1]>9)
            lcd.setCursor(2,1);
          else{
            lcd.setCursor(2,1);
            lcd.print("0");
            lcd.setCursor(3,1);
          }
          lcd.print(ValueState[1]);
          break;
  
        //Bass
        case 2:
          lcd.setCursor(0,0);
          lcd.print("BASS            ");
          if(ValueState[2]>9)
            lcd.setCursor(2,1);
          else{
            lcd.setCursor(2,1);
            lcd.print("0");
            lcd.setCursor(3,1);
          }
          lcd.print(ValueState[2]);
          break;
  
        //Treble
        case 3:
          lcd.setCursor(0,0);
          lcd.print("TREBLE          ");
          if(ValueState[3]>9)
            lcd.setCursor(2,1);
          else{
            lcd.setCursor(2,1);
            lcd.print("0");
            lcd.setCursor(3,1);
          }
          lcd.print(ValueState[3]);
          break;
  
        //Atenuation Right
        case 4:
          lcd.setCursor(0,0);
          lcd.print("ATTENUATION R   ");
          if(ValueState[4]>9)
            lcd.setCursor(2,1);
          else{
            lcd.setCursor(2,1);
            lcd.print("0");
            lcd.setCursor(3,1);
          }
          lcd.print(ValueState[4]);
          break;
  
        //Atenuation Left
        case 5:
          lcd.setCursor(0,0);
          lcd.print("ATTENUATION L   ");
          if(ValueState[5]>9)
            lcd.setCursor(2,1);
          else{
            lcd.setCursor(2,1);
            lcd.print("0");
            lcd.setCursor(3,1);
          }
          lcd.print(ValueState[5]);
          break;
  
        //Input
        case 6:
          lcd.setCursor(0,0);
          lcd.print("INPUT SELECTION ");
          if(ValueState[6]>9)
            lcd.setCursor(2,1);
          else{
            lcd.setCursor(2,1);
            lcd.print("0");
            lcd.setCursor(3,1);
          }
          lcd.print(ValueState[6]);
          break;
        default:;
      };

  
  recebeWIFI();
  //if((millis()-timeTxcurent)>=timeTX){
    //timeTxcurent=millis();
    //enviaWIFI();  
  //}
  
  

}
void inic() {
  //Serial.println("startInic");

  digitalWrite(GREEN_LED, HIGH);

  //inicializa o ganhoIn
  envairi2c(functionSelect[1], matGainIn[ValueState[1]]);

  //Volume
  envairi2c(functionSelect[0], matVol[ValueState[0]]);

  //Bass
  envairi2c(functionSelect[2], matBass[ValueState[2]]);

  //Treble
  envairi2c(functionSelect[3], matTreble[ValueState[3]]);

  //Atenuação Right
  envairi2c(functionSelect[4], matAtt[ValueState[4]]);

  //Atenuação Left
  envairi2c(functionSelect[5], matAtt[ValueState[5]]);

  
  digitalWrite(GREEN_LED, LOW);

}

void envairi2c(byte funcao, byte value) {
  //WDTCTL = WDTPW | WDTHOLD;
  digitalWrite(RED_LED, HIGH);
  Wire.beginTransmission(B00000001); // endereço
  Wire.beginTransmission(adress); // endereço
  Wire.write(funcao);
  Wire.write(value);
  Wire.endTransmission();
  delay(50);
  //digitalWrite(P4_2,HIGH);
  //digitalWrite(P4_1,HIGH);
  digitalWrite(RED_LED, LOW);
}

void recebeSerial() {
  //int i=0;
  if (Serial.available()>0){
    
    RxSerial[0] = Serial.read();
    delay(10);
    RxSerial[1] = Serial.read();
    delay(10);
    RxSerial[2] = Serial.read();
    
    for(int i=0; i<7;i++){
      if (RxSerial[0]==functionSelect[i]){
        //ValueState[i]=int(RxSerial[1]);
        envairi2c(RxSerial[0],RxSerial[1]);
        //for(int j=0;j<maxMin[i];i++)
          //if(RxSerial[1]==  
          ValueState[i]=int(RxSerial[2]);
      }
    }
    
  }
  //RxSerial[0]=0;
  //RxSerial[1]=0;
}

void encodeR(){

  int lerB=digitalRead(B);
 
  if(lerA==lerB){
      //Serial.print(lerA);
      //Serial.println(lerB);
      //if (valorEnc != 0)
      //valorEnc--;
      stateTemp=false;
      //digitalWrite(GREEN_LED,LOW);
  }
  else {
    //Serial.println("decrementa"); 
    //if (valorEnc != 14)
          //valorEnc++;
    //digitalWrite(GREEN_LED,HIGH);
   stateTemp=true;
  }
  flagSend=true;
}

void enviaWIFI(){
  //if(flagChegou==0){
    Serial1.println("AT+CIPSEND=0,18");
    delay(20);
    for(int i=0;i<6;i++){
      Serial1.println(ValueState[i]);
      //Serial.println("entrou");
      }
      Serial1.println("+++");
      delay(1000);
  //}
}

void recebeWIFI(){
if (Serial1.available() > 0) {
    //delay(100);
    //flagChegou=1;
    leitura = Serial1.read();
    
    Serial.print(leitura);
    //Serial.print(int(leitura));
    RxWIFI.concat(leitura);
    tamanho++;

    if (RxWIFI.substring(0, 7) == "+IPD,0,") {
        valida=true;
      }
      if(valida){
        if(leitura==':' ){
          in=tamanho;
        }
          
        if(leitura=='_'){
          //out=tamanho;
          RxByte[i]=RxWIFI.substring(in, tamanho).toInt();
          i++;
          if(i==3){
            i=0;
          //Serial.print("aki");
          //Serial.println(RxByte[0]);
          //Serial.println(RxByte[1]);
          //Serial.println(RxByte[2]);
          //dado coletado e enviando para o equ
          envairi2c(RxByte[0],RxByte[1]);
          for(int j=0; j<7;j++){
            //Serial.print("aki");
              
              if (RxByte[0]==functionSelect[j]){
                Serial.println(RxByte[0]);
                Serial.println(RxByte[1]);
                Serial.println(RxByte[2]);
              //ValueState[i]=int(RxSerial[1]);
              //Serial.print("emm");
              
              //for(int j=0;j<maxMin[i];i++)
              //if(RxSerial[1]==  
              ValueState[j]=int(RxByte[2]);
              flagChegou=0;
              break;
              
            }
          }//end for que envia para o equ
          
          }
        }//atendeu e encontrou o _
      }//end validado

    if (leitura == '\n' || leitura=='\r') {
      
      RxWIFI = "";
      valida=false;
      tamanho=0;
    }

  }//end available

  
  
}

void WifiTCPinit(){
   Serial1.print("AT+RST\r\n");
   delay(2000);
   Serial1.print("AT+CWMODE=1\r\n");
   delay(2000);
   Serial1.print("AT+CWJAP=\"Roberto\",\"senha123\"\r\n");
   delay(8000);
   Serial1.print("AT+CIPMUX=1\r\n");
   delay(2000);
   Serial1.print("AT+CIPSERVER=1,4000\r\n");
   delay(2000);
}

