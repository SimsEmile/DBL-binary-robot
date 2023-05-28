import RPi.GPIO as GPIO
import time

# Set GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Set GPIO pins for trigger and echo
TRIG_PIN = 23
ECHO_PIN = 24

def measure_distance():
    # Set trigger pin as output and echo pin as input
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    # Set trigger pin to low to ensure clean signal
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)

    # Send a 10us pulse to trigger pin
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Wait for echo pin to go high
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for echo pin to go low
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate pulse duration and convert to distance (in cm)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    # Round distance to two decimal places
    distance = round(distance, 2)

    return distance

try:
    while True:
        # Measure distance and print the result
        dist = measure_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
