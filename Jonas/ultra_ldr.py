#sudo apt-get install fswebcam
import RPi.GPIO as GPIO
import time
import os
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
#ultrasone
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
#motor
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
#ldr
GPIO.setup(22,GPIO.IN)
GPIO.setup(27,GPIO.IN)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.IN)
status1 = ""
status2 = ""
status3 = ""
status4 = ""
counter = 4

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

        #meten vanafstand
        distance = measure()
        if(distance <= 30):
            print("car!!!")
            if (GPIO.input(17)==0 and status1 != "bezet"):
                print("bezet1")
                counter-=1
                status1 = "bezet"
                print(counter)

            elif (GPIO.input(17)==1 and status1 != ""):
                print("leeg")
                status1 = ""
                counter+=1
                print(counter)

            if (GPIO.input(27)==0 and status2 != "bezet"):
                print("bezet2")
                counter-=1
                status2 = "bezet"
                print(counter)

            elif (GPIO.input(27)==1 and status2 != ""):
                print("leeg")
                status2 = ""
                counter+=1
                print(counter)
            if (GPIO.input(5)==0 and status3 != "bezet"):
                print("bezet2")
                counter-=1
                status3 = "bezet"
                print(counter)

            elif (GPIO.input(5)==1 and status3 != ""):
                print("leeg")
                status3 = ""
                counter+=1
                print(counter)
            if (GPIO.input(6)==0 and status4 != "bezet"):
                print("bezet2")
                counter-=1
                status4 = "bezet"
                print(counter)

            elif (GPIO.input(6)==1 and status4 != ""):
                print("leeg")
                status3 = ""
                counter+=1
                print(counter)

            else:
                pass

            if (counter >= 1):
                os.system("fswebcam -r 1280x720 --no-banner image1.jpg")
                # nummerplaat checken

                #motor aansturen
                for i in range(100):
                    wave_drive(8,25,24,23)
                for i in range(100):
                    reverse_wave_drive(8,25,24,23)
                print(distance)

        #
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