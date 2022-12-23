#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from sense_hat import SenseHat
from gpiozero import LED

 
#GPIO SETUP
channel = 21
waterpump = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)                    #Digital output from soil sensor
GPIO.setup(waterpump, GPIO.OUT)                 #waterPump

led = LED(16)                      

#Initialise SenseHAT
sense = SenseHat()
sense.clear()
green = (0,255,0)
red = (255,0,0)

def callback(channel):
        if GPIO.input(channel):
                print("No Water Detected!")
                sense.show_message("Water Plants!!", text_colour = red)
                sense.clear(red)
                led.on()                      
                #GPIO.output(waterpump, True)                    #turn on waterPump
        else:
                print("Water Detected!")
                sense.show_message("All Good", text_colour = green)
                sense.clear(green)
                led.off()                         #turn off waterPump
                #GPIO.output(waterpump, False)
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
while True:
        time.sleep(1)       
        
