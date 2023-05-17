#import GPIO as GPIO
#import time

#set GPIO pin numbers
#S2 = 23
#S3 = 24
#OUT = 18
#set GPIO pins as output
#GPIO.setup(S2, GPIO.OUT)
#GPIO.setup(S3, GPIO.OUT)

#set GPIO pins as input
#GPIO.setup(OUT, GPIO.IN)

encoding = int(input())
if encoding >= 32:
    print('Lower intellect person, you were asked for a number between 0 and 15, please provide such as to not look dumb lmao')
    quit()
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
  pass

def colorCheck():
  if (color <= 50 and binary[binary_index] == 0) or (color >= 715 and binary[binary_index] == 1):
    #start = time.time()
    return True
  return False

def Arm():
    pass
  #time.sleep(0.5)
  #Move the arm a specific amount of degrees, so that it gets the disk inside

def NextNumber():
  if binary_index != 0:
    binary_index -= 1
  else:
    print('The binary encoding is finished')
    quit()

def Colorreading():
  
  num_cycles = 10
  
  #red (low low)
  intensity = 0
  #GPIO.setup(S2, GPIO.LOW)
  #GPIO.setup(S3, GPIO.LOW)
  for i in range(num_cycles):
    #intensity += GPIO.input(OUT)
  #intensity = intensity /num_cycles
  #red = intensity*255
    a = 1
  #blue (low high)
  intensity = 0
  #GPIO.setup(S2, GPIO.LOW)
  #GPIO.setup(S3, GPIO.HIGH)
  for i in range(num_cycles):
      a = 1
    #intensity += GPIO.input(OUT)
  #intensity = intensity /num_cycles
  #blue = intensity*255
  
  #green (high high)
  #intensity = 0
  #GPIO.setup(S2, GPIO.HIGH)
  #GPIO.setup(S3, GPIO.HIGH)
  for i in range(num_cycles):
      a = 1
    #intensity += GPIO.input(OUT)
  #intensity = intensity /num_cycles
  #green = intensity*255
  
  #return red + blue + green

while exitcode == None:
  if ultrasoundcheck():
    color = Colorreading()
    if colorCheck():
      Arm()
      NextNumber()
    else:
      pass
  #elif (start - time.time()) >= 30:
    #Exception('Belt broken, commencing shutdown')
      




print("Color readings are different from described color, let it pass through")