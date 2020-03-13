import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

def Read_channel(number_of_Channel):
 adc = spi.xfer2([1,number_of_Channel<<4,0])
 data = ((adc[1]) << 8) + adc[2]
 return data

def Convert_to_Volts(data):
 volts = (data * 3.3) / float(1023)
 #volts = round(volts,4)  #округдение чисел
 return volts

while 1:
 channel_1 = Read_channel(8)
 channel_1_v = Convert_to_Volts(channel_1)
 print(channel_1_v)
 channel_2 = Read_channel(9)
 channel_2_v = Convert_to_Volts(channel_2)
 print(channel_2_v)
 time.sleep(1)
