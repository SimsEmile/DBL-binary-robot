# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:32:32 2023

@author: ansea
"""

import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_vl6180x

i2c = busio.I2C(board.SCL, board.SDA) #set up the TOF2 sensor's i2c bus
#set GPIO
GPIO.setmode(GPIO.BCM) #set pins to GPIO value

#set motors up, using dictionnaries
Motor1 = {'EN': 25, 'input1': 24, 'input2': 23} #motor 1 is used for the windmill which retrieves the disks

#setup distance sensor object to read the distance
sensor = adafruit_vl6180x.VL6180X(i2c)

#set GPIO pin numbers for the color sensor
S2 = 16
S3 = 20
OUT = 21

#set GPIO pins for the color sensor as output
GPIO.setup(S2, GPIO.OUT)
GPIO.setup(S3, GPIO.OUT)

#set GPIO pins for the color sensor as input
GPIO.setup(OUT, GPIO.IN)

#set global values
start = time.time()

# initialize functions

def calibration(): #calibrate white and black thresholds depending on lighting, can change at every iteration of the code
   black = BLACK()
   white = WHITE()
   return black, white

def BLACK(): #black threshold, using the Blue(), Red() and Green() functions, and taking the maximum of them all to create a high threshold, to avoid false negatives
   blue = 0
   red = 0
   green = 0
   print("preparing for black color test, press y to start, or no to shutdown")
   blacktest = input()
   if blacktest == "y":
      for loop in range(10):
         bluenew = Blue()
         blue = max(blue, bluenew)
         rednew = Red()
         red = max(red, rednew)
         greennew = Green()
         green = max(green, greennew)
      Black_Color = blue + green + red
      print(Black_Color)
   else:
      quit()
   time.sleep(1)
   return Black_Color

def WHITE(): #white threshold, taking the average and reducing by certain amount to avoid lower values being ignored, works the same as the BLACK function
   print("are ya ready for the white disk test now?")
   whitetest = input()
   if whitetest == "y":
      blue1 = 0
      red1 = 0
      green1 = 0
      for loop in range(10):
         blue1 += Blue()/10
         red1 += Red()/10
         green1 += Green()/10
      White_Color = blue1 + red1 + green1
      print(White_Color)
   else:
      quit()
   return White_Color

def ultrasoundcheck(): #check if a shape which is sufficiently high to be recognized as a disk, which gets analyzed as well
    range_mm = sensor.range #checks distance of the highest object (belt or other) from the TOF2 sensor
    print("Range: {0}mm".format(range_mm)) 
    if range_mm <= 30: #range at which the disk will be detected
      first_time = time.time() #this is to check for if something longer than the disk is on the belt, so we ignore it
      while range_mm <= 20: #while the disk is under it, and also to check once the disk should be gone through
        range_mm = sensor.range
        if time.time() - first_time > 3: #if this is True, there is an issue, the disk should've gone through
          print("hello")
          time.sleep(20) #sleep for 20 seconds, to let the wrong disk through
          if sensor.range == range_mm: #if the range is the same, we can assume that the belt can have an issue, if the range is exafctly the same +/- 1
            print("belt is potentially stuck, or factory has tried to sabotage me too much, initiating shutdown") #create an exitcode
            quit() #leaves the code, stops the robot
      time.sleep(5.5) #wait for the disk to be under the color sensor
      colorCheck() #check if the disk is the correct color

def colorCheck():
  color = ColorReading() #reads color in frequency, and depending on the thresholds, white, black, or something else
  print(color)
  print(binary[binary_index])
  time.sleep(1)
  if (color == "black") and (binary[binary_index] == "0"): #if the disk is black and needed to display the current bit, get it
    print("gotcha bitch")
    time.sleep(1)
    Arm()
  elif (color == "white") and (binary[binary_index] == "1"): #if the disk is black and needed to display the current bit, get it
    print("gotcha bitch")
    time.sleep(5) #create a time buffer, as to not force the motor to be on for too long
    Arm() #call upon the arm function, which activates the windmill
  else:
    print("oopsie poopsie") #message to the terminal, informs user that the disk was a wrong one


def Arm(): #function to move the arm to retrieve the disk
  for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT) #sets all GPIO pins to output pins (information is sent out, not retrieved)

  EN1 = GPIO.PWM(Motor1['EN'], 100)

  EN1.start(0)
  time.sleep(5) #waits for the disk to be underneath, because we don't want it to be on too long, as not to waste battery. For the straight belt, this is only 5 seconds
  print ("FORWARD MOTION")
  EN1.ChangeDutyCycle(30) #changes the speed of the motor, activating it

  GPIO.output(Motor1['input1'], GPIO.HIGH)
  GPIO.output(Motor1['input2'], GPIO.LOW)
  time.sleep(5) #keep the motor on for 5 seconds, to limit its time being on

  print("Stop motors")
  EN1.ChangeDutyCycle(0) #turn the motor off

  NextNumber() #After moving the arm, we continue onto the next number


def NextNumber(): #goes onto the next bit to represent
  if binary_index != 0: #if we're done with the binary number representation, no need to continue. Else, we go onto the next bit
    binary_index -= 1
    start = time.time() #sets the timer up again, as we are in a new loop of the robot, to get the next disk
  else:
    exitcode = 'The binary encoding is finished' #if finished, give an exitcode, so that the main loop stops

def Red(): #check frequency of red from the color sensor
    NUM_CYCLES = 10
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    time.sleep(0.3)
    start_impulse = time.time()
    for impulse_count in range(NUM_CYCLES): # Measure the falling edge of the signal for the specified number of cycles
      GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start_impulse
    red  = NUM_CYCLES / duration
    return red

def Blue(): #check frequency of blue from the color sensor
    NUM_CYCLES = 10
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    time.sleep(0.3)
    start_impulse = time.time()
    for impulse_count in range(NUM_CYCLES): # Measure the falling edge of the signal for the specified number of cycles
      GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start_impulse
    blue = NUM_CYCLES / duration
    return blue

def Green(): #check frequency of green from the color sensor
    NUM_CYCLES = 10
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    time.sleep(0.3)
    start_impulse = time.time()
    for impulse_count in range(NUM_CYCLES): # Measure the falling edge of the signal for the specified number of cycles
      GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start_impulse
    green = NUM_CYCLES / duration
    return green

    # if green>12000 and blue>12000 and red>12000:
def ColorReading(): #gets the color data from the color sensor, each filtered for a primary color
    print(White_Color)
    print(Black_Color)
    red = Red()
    blue = Blue()
    green = Green()
    print(red + green + blue)
    if green + blue + red >= White_Color: #threshold calibrated at the start for white
      return "white"
    #elif green <7000 and blue < 7000 and red < 7000: #threshold calibrated at the start for black
    elif green + blue + red <= Black_Color:
      return "black"
    else:
      print("Color readings are different from described color, let it pass through") #if it's neither black or white, we tell the terminal to inform the user, if it might be a mistake
      return "neither black nor white"


Black_Color, White_Color = calibration() #get values for black and white, calibrated for the current iteration of the robot
White_Color -= 6000 #getting threshold down to avoid false negatives of white

#encoding of the binary number
encoding = int(input()) #gets input from user
if encoding >= 32: #higher than 31 can't be represented
  Exception('0 to 31 I said, come on man')
elif encoding < 0:
  Exception("Dude, how am I gonna represent a negative number, think Human think")
print(encoding) #used to inform the user of it's choice to represent, to confirm it to them

binary = "" #string to represent the binary encoding
while encoding != 0: #formula to get the encoding from a decimal number
  binary = str(encoding%2) + binary
  encoding = encoding//2

print(binary) #final binary encoding, to write down to check later

exitcode = None
binary_index = len(binary)-1 #number is represented from bottom to down on the ramp, so we start at the end of the encoding, for 2**0
print(binary_index)
time.sleep(1)
start = time.time() #global value refreshed to start fault detection for the belt.

while exitcode == None:
  # if nothing is detected for more than 45 sec, which if the belt is working like an actual factory belt, should be seeing a disk each 20-25 seconds
  if (time.time() - start) >= 45:
    exitcode = 'Belt broken, commencing shutdown'
  else:
    ultrasoundcheck()

GPIO.cleanup() #clean up GPIO pins to avoid problems if we use the pi for something else after
print(exitcode) #print exitcode if it existed
quit()

