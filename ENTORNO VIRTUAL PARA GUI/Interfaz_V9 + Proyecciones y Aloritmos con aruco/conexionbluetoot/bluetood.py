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
    # Verificar si hay datos disponibles para leer
    if ser.in_waiting > 0:
        # Leer los datos disponibles
        data = ser.readline().decode('utf-8')
        return data
    else:
        return None

while True:
    # Adquirir datos cada 100 ms
    time.sleep(0.1)
    # Recuperamos los datos de los sensores si están disponibles
    sensor_data = retrieveData()
    if sensor_data is not None:
        print("Datos de los sensores:", sensor_data)

# Cierra la conexión serial cuando termina el programa
ser.close()
