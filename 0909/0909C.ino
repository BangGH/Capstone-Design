void setup() {
  Serial.begin(115200);

  pinMode(2,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,INPUT);
}

void loop() {
  int readValue = digitalRead(5);
  Serial.println(readValue);

  if(readValue==HIGH){
    digitalWrite(2,HIGH);
    digitalWrite(4,HIGH);
  }
  else{
    digitalWrite(2,LOW);
    digitalWrite(4,LOW);
  }
}