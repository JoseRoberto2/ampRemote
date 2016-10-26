char comp1[10] = "+IPD,0,";
char comp2[2] = "\n";
int contSer = 0;
int contSer2 = 0;
int ValueState[7] = {07, 00, 07, 07, 01, 01, 00};
int tamanho = 0;
int RxByte[4];
//char parametro;
String RxWIFI;
char leitura;
boolean valida = false;
String Validado;
boolean validade2=false;
int i=0;
int in;
int out;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
  pinMode(RED_LED, OUTPUT);
  digitalWrite(RED_LED, HIGH);

  Serial.println("inicando");
  WifiTCPinit();
  digitalWrite(RED_LED, LOW);
  pinMode(PUSH1, INPUT_PULLUP);

}

void loop() {


  if (Serial1.available() > 0) {
    leitura = Serial1.read();
    delay(200);
    Serial.print(leitura);
    //Serial.print(int(leitura));
    RxWIFI.concat(leitura);
    tamanho++;

    if (RxWIFI.substring(0, 7) == "+IPD,0,") {
        //Serial.print("validado");
        //Serial.print("RX");
        //Serial.print(contSer);
        //contSer++;
        valida=true;
      }
      //string.toInt();
      if(valida){
        //if(leitura=='(' ){
        if(leitura==':' || leitura==','){
          Serial.print(tamanho);
          Serial.print("aki");
          in=tamanho;
          //valida2=true
        }

        //if(leitura=='_'){
        if(leitura=='_' || leitura==')'){
          
          Serial.print(tamanho);
          Serial.print("passou");
          out=tamanho;
          String data;
          RxByte[i]=RxWIFI.substring(in, out).toInt();
          i++;
          if(i==3){
            i=0;
            //enviar para o equ
          
          Serial.println(RxByte[0]);
          Serial.println(RxByte[1]);
          Serial.println(RxByte[2]);
          }
        }
      }

    //if (leitura == '\n' || leitura=='\r') {
    if (leitura == '\n' || leitura=='\r') {
      //if (RxWIFI.substring(0, 7) == "+IPD,0,") {
        //Serial.print("validado");
        //Serial.print("RX");
        //Serial.print(contSer);
        //contSer++;
      //}
      
      
      RxWIFI = "";
      valida=false;
      tamanho=0;
    }

  }//end available
  //  if(valida==1){
  //    Serial.print("validado");
  //    valida=0;
  //    Serial.print(RxWIFI.substring(0,7));
  //    if(RxWIFI.substring(0,7)=="+IPD,0,"){
  //      Serial.print("RX");
  //    }
  //    RxWIFI="";
  //  }

  //  else{
  //  Serial.print(RxWIFI.substring(0,7));
  //  if(RxWIFI.substring(0,6)=="+IPD,0,"){
  //    Serial.print("validado");
  //  }
  //  }


}//end loop


void WifiTCPinit() {
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
