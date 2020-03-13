# Servo Control
print ("hello")
import time
import wiringpi
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)
delay_period = 0.01
while True:
 for pulse in range(100, 180, 1):
  wiringpi.pwmWrite(18, pulse)
  wiringpi.pwmWrite(13, pulse)
  time.sleep(1)
  
 for pulse in range(180, 100, -1):
  wiringpi.pwmWrite(18, pulse)
  wiringpi.pwmWrite(13, pulse)
  time.sleep(1)
