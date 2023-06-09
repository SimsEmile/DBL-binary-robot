import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}
Motor2 = {'EN': 11, 'input1': 9, 'input2': 10}

for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)

EN1 = GPIO.PWM(Motor1['EN'], 100)
EN2 = GPIO.PWM(Motor2['EN'], 100)

EN1.start(0)
EN2.start(0)

print ("FORWARD MOTION")
EN1.ChangeDutyCycle(30)
EN2.ChangeDutyCycle(80)

GPIO.output(Motor1['input1'], GPIO.HIGH)
GPIO.output(Motor1['input2'], GPIO.LOW)

GPIO.output(Motor2['input1'], GPIO.HIGH)
GPIO.output(Motor2['input2'], GPIO.LOW)

sleep(50)

print ("STOP")
EN1.ChangeDutyCycle(0)
EN2.ChangeDutyCycle(0)

sleep(5)

GPIO.cleanup()