char comp1[10]="+IPD,0,8:";
int contSer=0;
int ValueState[7]={07,00,07,07,01,01,00};
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
  pinMode(RED_LED,OUTPUT);
  digitalWrite(RED_LED,HIGH);
  
  Serial.println("inicando");
  WifiTCPinit();
  digitalWrite(RED_LED,LOW);
  pinMode(PUSH1,INPUT_PULLUP);

}

void loop() {
  char leitura;
  // put your main code here, to run repeatedly:
   if (Serial1.available()>0){
    leitura = Serial1.read();
    //Serial.print(leitura);
    Serial.print(leitura);
    if(leitura==comp1[contSer]){
      contSer++;
      if(contSer==8){
      Serial.print("passou");
      //delay(100);
      //for(int i=0; i<50;i++){
        
        Serial1.println("AT+CIPSEND=0,21");
        delay(20);
        for(int i=0;i<7;i++){
          Serial1.println(ValueState[i]);
        //Serial.println("entrou");
        }
        Serial1.println("+++");
        
        delay(1000);
      //}
      //delay(300);
      contSer=0;
      }
    }
    else{
      contSer=0;
    }
  }
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
