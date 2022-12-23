#!/usr/bin/python3

import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import sys
import time
from sense_hat import SenseHat
import logging
from dotenv import dotenv_values

#Initialise RPi I2C
import smbus
import time

address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)

#Initialise SenseHAT
sense = SenseHat()
sense.clear()

#load MQTT configuration values from .env file
config = dotenv_values(".env")

#configure Logging
logging.basicConfig(level=logging.INFO)

# Define event callbacks for MQTT
def on_connect(client, userdata, flags, rc):
    logging.info("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    logging.info("Message Sent ID: " + str(mid))

mqttc = mqtt.Client(client_id=config["clientId"])

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# parse mqtt url for connection details
url_str = sys.argv[1]
print(url_str)
url = urlparse(url_str)
base_topic = url.path[1:]

# Configure MQTT client with user name and password
mqttc.username_pw_set(config["username"], config["password"])

#Connect to MQTT Broker
mqttc.connect(url.hostname, url.port)
mqttc.loop_start()

#Set Thingspeak Channel to publish to
topic = "channels/"+config["channelId"]+"/publish"

# Publish a message to channel every 15 seconds
while True:
    try:
        bus.write_byte(address,A0)
        value = bus.read_byte(address)
        value = (round(value/256*100,2))        #8bit ADC
        #print(round(value/256*100,2))
        #time.sleep(1)

        temp=round(sense.get_temperature(),2)
        humidity=round(sense.get_humidity(),2)
        pressure=round(sense.get_pressure(),2)
        payload=f"field1={temp}&field2={humidity}&field3={pressure}&field4={value}"
        mqttc.publish(topic, payload)
        time.sleep(int(config["transmissionInterval"]))
    except:
        logging.info('Interrupted')
        
