import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT) #GPIO2
while True:
	GPIO.output(2,GPIO.HIGH)
	print("high")
	time.sleep(1)
	GPIO.output(2,GPIO.LOW)
	print("low")
	time.sleep(1)


