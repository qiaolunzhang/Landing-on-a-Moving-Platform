int Delay1_zhou = 8; 
int Delay2_zhou = 12; 
int pwm3=3;
int pwm5=5;
unsigned long duration3;
unsigned long duration5;
void setup(){
Serial.begin(9600);
pinMode(pwm3,INPUT);
pinMode(pwm5,INPUT);
pinMode(Delay1_zhou, OUTPUT); 
pinMode(Delay2_zhou, OUTPUT); 
}
void loop(){
  duration3=pulseIn(pwm3,HIGH);
  duration5=pulseIn(pwm5,HIGH);
  Serial.print("CH3:");
  Serial.println(duration3);
  Serial.print("CH5:");
  Serial.println(duration5);

  if(duration3>1500){
  digitalWrite(Delay1_zhou, LOW);
  delay(100);
  digitalWrite(Delay2_zhou, HIGH);
  delay(100);
  }
  else{
    if(duration5>1500){
  digitalWrite(Delay1_zhou, HIGH);
  delay(100);
  digitalWrite(Delay2_zhou, LOW);
    }
    else{
  digitalWrite(Delay1_zhou, HIGH); 
  delay(100);
  digitalWrite(Delay2_zhou, HIGH); 
  delay(100);
    }
  }
  }
