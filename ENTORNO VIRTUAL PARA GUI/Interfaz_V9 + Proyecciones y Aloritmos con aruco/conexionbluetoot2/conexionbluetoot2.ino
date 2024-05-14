int pot1 = A0; // Potenciómetro 1 conectado a A0
int pot2 = A1; // Potenciómetro 2 conectado a A1

void setup() {
  Serial.begin(9600); // Inicia la comunicación serial para depuración
  pinMode(pot1, INPUT);
  pinMode(pot2, INPUT);
}

void loop() {
  int dataPot1 = analogRead(pot1); // Lee el valor del potenciómetro 1
  int dataPot2 = analogRead(pot2); // Lee el valor del potenciómetro 2
  
  // Imprime los datos de los potenciómetros en el monitor serial
  Serial.print("Pot1:");
  Serial.println(dataPot1);
  Serial.print("Pot2:");
  Serial.println(dataPot2);
  
  delay(100); // Espera 100 milisegundos antes de la próxima lectura
}
