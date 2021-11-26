#!/usr/bin/python

import time
import MySQLdb
import paho.mqtt.client as mqtt

# Functions
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
    # print('Received a message on topic: ' + msg.topic + '; message: ' + msg.payload)
    if msg.topic.startswith('Parking/Plaats1'):
        if msg.payload == 'empty':
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("DELETE FROM `parkeergarage` WHERE `parkeerplaats` = 1")
        else:
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("INSERT INTO parkeergarage(nummerplaat, parkeerplaats) VALUES(\"{}\", 1)".format(msg.payload))
    if msg.topic.startswith('Parking/Plaats2'):
        if msg.payload == 'empty':
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("DELETE FROM `parkeergarage` WHERE `parkeerplaats` = 2")
        else:
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("INSERT INTO parkeergarage(nummerplaat, parkeerplaats) VALUES(\"{}\", 2)".format(msg.payload))            
    if msg.topic.startswith('Parking/Plaats3'):
        if msg.payload == 'empty':
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("DELETE FROM `parkeergarage` WHERE `parkeerplaats` = 3")
        else:
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("INSERT INTO parkeergarage(nummerplaat, parkeerplaats) VALUES(\"{}\", 3)".format(msg.payload))
    if msg.topic.startswith('Parking/Plaats4'):
        if msg.payload == 'empty':
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("DELETE FROM `parkeergarage` WHERE `parkeerplaats` = 4")
        else:
            print(msg.topic + ': ' + msg.payload)
            cursor.execute("INSERT INTO parkeergarage(nummerplaat, parkeerplaats) VALUES(\"{}\", 4)".format(msg.payload))
    database.commit()
            
#Verbinden met de database
database = MySQLdb.connect(host="localhost", user="pi", passwd="raspberry", db="mydb")

#database select en cleanup
cursor = database.cursor()
#cursor.execute("TRUNCATE TABLE parkeergarage") #tabel leegmaken na herstart

# broker and client declaration
broker = 'test.mosquitto.org'
client = mqtt.Client('PI_LM2') #client name

# bind callback functions
#client.on_connect=on_connect
client.on_log = on_log
#client.on_disconnect = on_disconnect
client.on_message = on_message

# connect with broker
print('Connecting to broker ', broker)
client.connect(broker)
client.loop_start() #start loop_start

#subscribe to topic on broker
client.subscribe('Parking/Plaats1') #channel or topic
client.subscribe('Parking/Plaats2') #channel or topic
client.subscribe('Parking/Plaats3') #channel or topic
client.subscribe('Parking/Plaats4') #channel or topic

try:
    while True:
        pass
except KeyboardInterrupt:
    client.loop_stop() #stop loop
    client.disconnect()
