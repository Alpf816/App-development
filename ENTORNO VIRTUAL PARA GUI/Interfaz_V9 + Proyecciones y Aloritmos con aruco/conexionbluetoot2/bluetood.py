import serial
import time

# Cambia el nombre del puerto COM y el baudrate según sea necesario
ser = serial.Serial("COM4", 9600, timeout=1)

# Verificar si la conexión serial se estableció correctamente
if ser.isOpen():
    print("Conexión serial establecida correctamente.")
else:
    print("No se pudo establecer la conexión serial.")

def retrieveData():
    # Envía un comando al Arduino para solicitar los datos de los sensores
    ser.write(b'1')
    # Lee la respuesta del Arduino
    data = ser.readline().decode('ascii')
    return data

while True:
    # Adquirir datos cada 100 ms
    time.sleep(0.1)
    # Recuperamos los datos de los sensores y los imprimimos
    sensor_data = retrieveData()
    print("Datos de los sensores:", sensor_data)

# Cierra la conexión serial cuando termina el programa
ser.close()
