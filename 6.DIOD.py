from RPi import GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

while True:
  GPIO.output(23, True)
  sleep(0.5)
  GPIO.output(23, False)
  sleep(0.5)

