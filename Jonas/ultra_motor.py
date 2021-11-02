import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

def measure():
    GPIO.output(17, 1)
    time.sleep(0.00001)
    GPIO.output(17, 0)

    StartTime = time.time()
    StopTime = time.time()

    while (GPIO.input(18)==0):
        StartTime = time.time()

    while (GPIO.input(18)==1):
        StopTime = time.time()

    timepassed = StopTime - StartTime
    distance = (timepassed * 17000)
    return distance

def wave_drive(pin1,pin2,pin3,pin4):
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin4, 0)
    GPIO.output(pin1, 1)
    time.sleep(0.01)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 1)
    time.sleep(0.01)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 1)
    time.sleep(0.01)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 1)
    time.sleep(0.01)

def reverse_wave_drive(pin1,pin2,pin3,pin4):
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin2, 0)
    GPIO.output(pin1, 1)
    time.sleep(0.01)
    GPIO.output(pin1, 0)
    GPIO.output(pin4, 1)
    time.sleep(0.01)
    GPIO.output(pin4, 0)
    GPIO.output(pin3, 1)
    time.sleep(0.01)
    GPIO.output(pin3, 0)
    GPIO.output(pin2, 1)
    time.sleep(0.01)

try:
    while True:
        distance = measure()
        if(distance <= 30):
            print("car!!!")
            for i in range(100):
                wave_drive(8,25,24,23)
            for i in range(100):
                reverse_wave_drive(8,25,24,23)
            print(distance)
        if(distance > 30):
            print("no car")
            print(distance)
            GPIO.output(8, 0)
            GPIO.output(25, 0)
            GPIO.output(24, 0)
            GPIO.output(23, 0)
        time.sleep(1)
        

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
