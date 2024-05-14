#include <SoftwareSerial.h>

SoftwareSerial HC06(0, 1);  // RX pin 0, TX pin 1
int pot1 = A0;              // Potenciómetro 1 conectado a A0
int pot2 = A1;              // Potenciómetro 2 conectado a A1

void setup() {
  HC06.begin(9600);  // Inicia la comunicación serial con el módulo Bluetooth
  pinMode(pot1, INPUT);
  pinMode(pot2, INPUT);

  // Inicializar pines digitales como entradas
  for (int pin = 2; pin <= 12; pin++) {
        pinMode(pin, INPUT_PULLUP);
  }

  HC06.println("Ready!!!");  //Send something to just start comms. This will never be seen.
}

void loop() {
  int dataPot1 = analogRead(pot1);  // Lee el valor del potenciómetro 1
  int dataPot2 = analogRead(pot2);  // Lee el valor del potenciómetro 2

  // Envía los datos de los potenciómetros a través de Bluetooth
  HC06.print("Pot1:");
  HC06.println(dataPot1);
  HC06.print("Pot2:");
  HC06.println(dataPot2);

  // Leer y enviar el estado de cada pin digital
  for (int i = 2; i <= 13; i++) {
    HC06.print("DI");
    HC06.print(i);
    HC06.print(":");
    HC06.println(digitalRead(i));
  }

  delay(200);  // Espera 200 milisegundos antes de la próxima lectura
}
