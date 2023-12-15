import serial
import time

dev = serial.Serial("COM3",9600)
time.sleep(1)
while True:
    cad =dev.readline().decode('ascii')
    print(cad)
    print("**********************")