char cmd;

void setup() {
  
  // 시리얼 통신 시작 (boadrate: 9600)
  Serial.begin(115200);
  pinMode(2,OUTPUT);
  pinMode(4,OUTPUT);
}

void loop() {

  // 컴퓨터로부터 시리얼 통신이 전송되면, 한줄씩 읽어와서 cmd 변수에 입력
  if(Serial.available()){
    cmd = Serial.read(); 

    if(cmd=='a'){
      digitalWrite(2,HIGH);
      digitalWrite(4,LOW);
      delay(100);
    }
    else if(cmd=='b'){
      digitalWrite(2,LOW);
      digitalWrite(4,HIGH);
      delay(100);
    }
  }
}