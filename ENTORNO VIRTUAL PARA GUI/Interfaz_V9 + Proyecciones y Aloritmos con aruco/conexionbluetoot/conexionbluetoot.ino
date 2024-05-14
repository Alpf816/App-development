#include <SoftwareSerial.h>

SoftwareSerial HC06(0, 1); // RX pin 0, TX pin 1
int pot1 = A0; // Potenciómetro 1 conectado a A0
int pot2 = A1; // Potenciómetro 2 conectado a A1
int DI2 = 2; // Pin digital 2
int DI3 = 3; // Pin digital 3
int DI4 = 4; // Pin digital 4
int DI5 = 5; // Pin digital 5
int DI6 = 6; // Pin digital 6
int DI7 = 7; // Pin digital 7
int DI8 = 8; // Pin digital 8
int DI9 = 9; // Pin digital 9
int DI10 = 10; // Pin digital 10
int DI11 = 11; // Pin digital 11
int DI12 = 12; // Pin digital 12
int DI13 = 13; // Pin digital 13


void setup() {
  //Serial.begin(9600); // Inicia la comunicación serial para depuración
  HC06.begin(9600); // Inicia la comunicación serial con el módulo Bluetooth
  pinMode(pot1, INPUT);
  pinMode(pot2, INPUT);
  pinMode(DI2, INPUT_PULLUP); // Establece el pin del selector como entrada con pull-up
  HC06.println("Ready!!!");//Send something to just start comms. This will never be seen.
  //Serial.println("Started");
}

void loop() {
  // Verifica el estado del selector
  if (digitalRead(DI2) == HIGH) {
    //Serial.println("Selector leído"); // Imprime si se lee el selector
    HC06.print("Selector leído:");
    // Si el selector está en una posición que permite la lectura y el envío de datos
    int dataPot1 = analogRead(pot1); // Lee el valor del potenciómetro 1
    int dataPot2 = analogRead(pot2); // Lee el valor del potenciómetro 2
    
    // Envía los datos de los potenciómetros a través de Bluetooth
    HC06.print("Pot1:");
    HC06.println(dataPot1);
    HC06.print("Pot2:");
    HC06.println(dataPot2);
    //Serial.print("Pot1:");
    //Serial.println(dataPot1);
    //Serial.print("Pot2:");
    //Serial.println(dataPot2);
  }
  
  delay(200); // Espera 200 milisegundos antes de la próxima lectura
}
