import RPi.GPIO as GPIO
import time
import os
import requests
import re
from simplepush import send
import paho.mqtt.client as mqtt

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
message_sent = 0
numberplate = ""

# Functions
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
    
def on_log(client, userdata, level, buf):
    print('log: ' + buf)
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print ('Connected OK with result code ' + str(rc))
    else:
        print('Bad connection with result code ' + str(rc))

def on_disconnect(client, userdata, flags, rc = 0):
    print ('Disconnected result code ' + str(rc))
    
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print('Received a message on topic: ' + msg.topic + '; message: ' + msg.payload)

# broker and client declaration
broker = 'test.mosquitto.org'
client = mqtt.Client('PI_LM1') #client name

# bind callback functions
#client.on_connect=on_connect
client.on_log = on_log
#client.on_disconnect = on_disconnect
client.on_message = on_message

# connect with broker
print('Connecting to broker ', broker)
client.connect(broker, 1883)
client.loop_start() #start loop_start

try:
    while True:
        if (counter == 0 and message_sent == 0):
            send('daU3Jy', 'Status Parking', 'Parking volzet', 'IOTAdv_LM')
            message_sent = 1

        if counter > 0:
            message_sent = 0

        #meten vanafstand
        distance = measure()
        if (GPIO.input(22)==0 and status1 != "bezet"):
            print("bezet1")
            counter-=1
            status1 = "bezet"
            client.publish('Parking/Plaats1', numberplate) 
            print(counter)

        elif (GPIO.input(22)==1 and status1 != ""):
            print("leeg 1")
            status1 = ""
            counter+=1
            client.publish('Parking/Plaats1', "empty")
            print(counter)

        if (GPIO.input(27)==0 and status2 != "bezet"):
            print("bezet2")
            counter-=1
            status2 = "bezet"
            client.publish('Parking/Plaats2', numberplate)
            print(counter)

        elif (GPIO.input(27)==1 and status2 != ""):
            print("leeg 2")
            status2 = ""
            counter+=1
            client.publish('Parking/Plaats2', "empty")
            print(counter)
            
        if (GPIO.input(5)==0 and status3 != "bezet"):
            print("bezet 3")
            counter-=1
            status3 = "bezet"
            client.publish('Parking/Plaats3', numberplate)
            print(counter)

        elif (GPIO.input(5)==1 and status3 != ""):
            print("leeg 3")
            status3 = ""
            counter+=1
            client.publish('Parking/Plaats3', "empty")
            print(counter)
            
        if (GPIO.input(6)==0 and status4 != "bezet"):
            print("bezet 4")
            counter-=1
            status4 = "bezet"
            client.publish('Parking/Plaats4', numberplate)
            print(counter)

        elif (GPIO.input(6)==1 and status4 != ""):
            print("leeg 4")
            status4 = ""
            counter+=1
            client.publish('Parking/Plaats4', "empty")
            print(counter)

        else:
            pass
            
        if(distance <= 30):
            print("car!!!")

            if (counter >= 1):
                os.system("fswebcam -r 1280x720 --no-banner image1.jpg")
                # nummerplaat checken
                regions = ['be'] # Change to your country
                with open('./image1.jpg', 'rb') as fp:
                    response = requests.post(
                        'https://api.platerecognizer.com/v1/plate-reader/',
                        data=dict(regions=regions),  # Optional
                        files=dict(upload=fp),
                        headers={'Authorization': 'Token 4c3b2d68309ebeccb621b762e2ecc6b09d72a7b5'})
                try:
                    plate = response.json()['results'][0]['plate']                    
                    # plate = "toyota"
                    if re.search(r'^[0-9][a-z]{3}[0-9]{3}$' , plate):
                        numberplate = ("{}-{}-{}".format(plate[0], plate[1:4], plate[4:]).upper())
                    elif re.search(r'^[a-z]{3}[0-9]{3}$|^[0-9]{3}[a-z]{3}$' , plate):
                        numberplate = ("{}-{}".format(plate[0:3], plate[3:]).upper())
                    else:
                        numberplate = (plate.upper())
                    #motor aansturen
                    for i in range(120):
                        wave_drive(8,25,24,23)
                    time.sleep(5)
                    for i in range(120):
                        reverse_wave_drive(8,25,24,23)
                    print(numberplate)
                    print(distance)
                except:
                    plate = "empty"

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
    client.loop_stop() #stop loop
    client.disconnect()    
    GPIO.cleanup()