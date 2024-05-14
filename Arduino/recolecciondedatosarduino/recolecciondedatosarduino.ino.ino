const int Pin0 = A0, Pin1 = A1;
int valorAnalogo0, valorAnalogo1;
unsigned long lastTime,sampleTime;
}
void setup() {
  // put your setup code here, to run once:
Serial.being(9600);
ValorAnalogo0 = 0;
ValorAnalogo1 = 0;
sampleTime = 10;
lastTime = millis();

}

void loop() {
  // put your main code here, to run repeatedly:
if(millis()-lastTime >=sampleTime)
{
lastTime = millis();
ValorAnalogo0 = analogRead(Pin0);
ValorAnalogo1 = analogRead(Pin1);

//se añade los valores a enviar al serial
Serial.println(scaling(ValorAnalogo0,0,1023,0,5));
Serial.println(scaling(ValorAnalogo1,0,1023,0,5));
}
}