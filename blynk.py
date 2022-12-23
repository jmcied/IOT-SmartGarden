import BlynkLib
from sense_hat import SenseHat
from time import sleep
import smbus
import time
from gpiozero import LED
import logging
from dotenv import dotenv_values

led = LED(19)

#BLYNK_AUTH = 'zj-N86Bt0NPXCMCawiW20soa4wV6L
config = dotenv_values(".env")

# initialize Blynk
blynk = BlynkLib.Blynk(config["BLYNK_AUTH"])

#initialise SenseHAT
sense = SenseHat()
sense.clear()

#Initialise I2C
address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)

# register handler for virtual pin V0 write event
@blynk.on("V0")
def v3_write_handler(value):
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    if buttonValue=="1":
        sense.clear(255,255,255)
    else:
        sense.clear()

@blynk.on("V5")
def v3_write_handler(value):
    waterPumpValue=value[0]
    print(f'Current waterPump value: {waterPumpValue}')
    if waterPumpValue=="1":
        led.on()
    else:
        led.off()    

# infinite loop that waits for event
while True:
    bus.write_byte(address,A0)
    value = bus.read_byte(address)
    waterValue = (round(value/256*100,2))
    blynk.run()
    blynk.virtual_write(1, round(sense.temperature,2)) #ADD THIS
    blynk.virtual_write(2, round(sense.get_pressure(),2))
    blynk.virtual_write(3, round(sense.get_humidity(),2))
    blynk.virtual_write(4, waterValue)

    sleep(0.5) # sleep for .5 second