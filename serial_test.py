
import serial
import time

ser = serial.Serial()
ser.port = 'COM4'
ser



import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

ports

for port, desc, hwid in sorted(ports):
	print("{}: {} [{}]".format(port, desc, hwid))
    
    
