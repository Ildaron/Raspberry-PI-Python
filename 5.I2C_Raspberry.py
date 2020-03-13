import RPi.GPIO as GPIO
from time import sleep
import time


import smbus
adr= 0x49
start=0x00
reg=0x00
print ("ok")
bus = smbus.SMBus(1)
while 1:
 bus.write_byte(adr,start)
 time.sleep(0.5)
 data=bus.read_word_data(adr,reg)
 data = ((data << 8) & 0xFF00) + (data >> 8)
 temp = (data / 32.0) / 8.0
 #print ('Temperature: {0:0.2f} *C'.format(temp))
 print("Tepm", temp, "C")
