#include <SoftwareSerial.h>

SoftwareSerial HC06(0, 1);  // RX pin 0, TX pin 1
int pot1 = A5;              // Potenciómetro 1 conectado a A0
int pot2 = A0;              // Potenciómetro 2 conectado a A1

void setup() {
  HC06.begin(9600);  // Inicia la comunicación serial con el módulo Bluetooth
  pinMode(pot1, INPUT);
  pinMode(pot2, INPUT);

  // Inicializar pines digitales como entradas
  for (int pin = 2; pin <= 12; pin++) {
    pinMode(pin, INPUT_PULLUP);
  }

  HC06.println("Ready!!!");  // Envía un mensaje inicial al encender.
}

void loop() {
  String dataString = "";  // Cadena para almacenar todos los datos

  int dataPot1 = analogRead(pot1);  // Lee el valor del potenciómetro 1
  int dataPot2 = analogRead(pot2);  // Lee el valor del potenciómetro 2
  dataString += "Pot1:" + String(dataPot1) + ",";
  dataString += "Pot2:" + String(dataPot2);

  // Leer y añadir el estado de cada pin digital a la cadena
  for (int i = 2; i <= 13; i++) {
    dataString += ","; // Agrega la coma antes de cada elemento
    dataString += "DI" + String(i) + ":" + digitalRead(i);
  }

  HC06.println(dataString);  // Envía todos los datos en una sola línea

  delay(200);  // Espera 200 milisegundos antes de la próxima lectura
}
