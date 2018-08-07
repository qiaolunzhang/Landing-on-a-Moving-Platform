int pwm3=3;
int pwm5=5;
unsigned long duration3;
unsigned long duration5;
int relay1=2;
int relay2=4;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pwm3,INPUT);
  pinMode(pwm5,INPUT);
  pinMode(relay1,OUTPUT);
  pinMode(relay2,OUTPUT);
  digitalWrite(relay1,LOW);
  digitalWrite(relay2,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  duration3=pulseIn(pwm3,HIGH);
  duration5=pulseIn(pwm5,HIGH);
  Serial.print("CH5:");
  Serial.println(duration3);
  Serial.print("CH7:");
  Serial.println(duration5);
  if(duration3>1700){
    if(duration5>1700){
      digitalWrite(relay1,LOW);
      delay(100);
      digitalWrite(relay2,HIGH);
      delay(100);
    }
    else if(duration5<1300){
      digitalWrite(relay1,HIGH);
      delay(100);
      digitalWrite(relay2,LOW);
      delay(100);
    }
    else {
      digitalWrite(relay1,LOW);
      delay(100);
      digitalWrite(relay2,LOW);
      delay(100);
    }
  }
  else {};
}
