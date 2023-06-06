# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:32:32 2023

@author: ansea
"""

import RPi.GPIO as GPIO
import time

#set GPIO
GPIO.setmode(GPIO.BCM)

#set motors up, using dictionnaries
Motor1 = {'EN': 25, 'input1': 24, 'input2': 23} #motor 1 is used for the windmill which retrieves the disks
Motor2 = {'EN': 11, 'input1': 9, 'input2': 10} #motor 2 is used for the belt, will be removed once not in use anymore

#set GPIO pin numbers for the color sensor
S2 = 5
S3 = 6
OUT = 18
#set GPIO pins for the ultrasound sensor
Trig_pin = 2
Echo_pin = 3
#set GPIO pins as output
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)

#set GPIO pins as input
GPIO.setup(OUT, GPIO.IN)

#set global values
start = time.time()

encoding = int(input())
if encoding >= 32:
  Exception('Too high a number asshole, pick sth else you bozo')
print(encoding)

binary = ''
while encoding//2 != 0:
  binary = str(encoding%2) + binary
  encoding = encoding//2

binary = str(encoding%2) + binary
print(binary)
exitcode = None
binary_index = len(binary)-1

def ultrasoundcheck():
  GPIO.setup(Trig_pin, GPIO.HIGH)
  time.sleep(0.0001)
  GPIO.setup(Trig_pin, GPIO.LOW)
  
  time_start = time.time()
  time_end = time.time()
  while GPIO.input(Echo_pin) == 0:
      time_start = time.time()
  while GPIO.input(Echo_pin) == 1:
      time_end = time.time()
      
  duration = time_end - time_start
  distance = duration * 17150
  start = time.time()    
  if 8.75 < GPIO.input(OUT) < 10.75: #Checks if the distance (including slight reading errors, is sufficient to consider there being a disk)
    time.sleep(3.5) #creates a time interval, after which normally, the disk would've already passes, and thus nothing would be retrieved
    if  8.75 < GPIO.input(OUT) < 10.75: #if there still is something after the time interval, we know that sth might be off
      print("Shape does not seem to be a disk, wait 10 seconds") #send message to terminal (which will be on the computer)
      time.sleep(10) #be inactive for 10 seconds, then proceed further with the rest.
    else:
      colorCheck()
  else:
    pass

def colorCheck():
  color = Colorreading()
  if (color == 'black' and binary[binary_index] == 0) or (color == "white" and binary[binary_index] == 1): #check if disc is the correct color we need
    start = time.time() #reset timer, as if time.time() - start = 30, we know there is a problem.
    time.sleep(0.5) #create a time buffer, as to not force the motor to be on for too long
    Arm() #call upon the arm function, which activates the windmill
  else:
    print("Color readings are different from described color, let it pass through") #message to the terminal, informs user that the disk was a wrong one

def Arm():
  for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT) #sets all GPIO pins to output pins (information is sent out, not retrieved)
    GPIO.setup(Motor2[x], GPIO.OUT) #same, except for the motor of the belt

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
    time.sleep(5)
    
    print("Stop motors")
    EN1.ChangeDutyCycle(0)
    EN2.ChangeDutyCycle(0)
    
    NextNumber() #After moving the arm, we continue onto the next number
  

def NextNumber():
  if binary_index != 0:
    binary_index -= 1
  else:
    exitcode = 'The binary encoding is finished'
    quit()

def Colorreading():
  temp = 1
  while(1):  
    NUM_CYCLES = 10
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   
   
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    

    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    
      
    # if green>12000 and blue>12000 and red>12000:
    if green + blue + red >= 95000:
      return "white"
    #elif green <7000 and blue < 7000 and red < 7000:
    elif green + blue + red <= 36000:
      return "black"
    else:
      print("Color readings are different from described color, let it pass through")
      return "neither black nor white"

while exitcode == None:
  if (time.time() - start) >= 30:
    exitcode = 'Belt broken, commencing shutdown'
  else:
    ultrasoundcheck()

GPIO.cleanup()
print(exitcode)
quit()
