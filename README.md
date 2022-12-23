# IOT-SmartGarden

The objective of this project was to create an environment where the user can monitor growing conditions within their greenhouse remotely. The main focus will be recording temperature, humidity and soil moisture levels. Actions can be carried out when conditions are met, too hot open door, soil too dry turn on waterpump.

Equipment used was a Raspberry Pi 3B, SenseHAT, Soil Moisture Sensor, 8bit ananlog to digital converter, NPN transistor, Diode, Mini water pump.

Running soil.py, once digital output threshold is met, a channel change is detected and channel turns high and turns on waterpump, once watering is sufficient and channel detects change to low pump turns off.

Using the ADC and implementing I2C protocol on RPi, an analog voltage can be read from sensor and converted to a digital equivalent. 
The resultant reading along with environment readings from the sensehat are sent to a thingspeak API so that a tweet and email can be sent to user when certain temperature and soil conditions are met.
A blynk web app was also created displaying temperature, humidity and soil conditions, A toggle switch could be used to turn on waterpump.

sources include:
https://www.instructables.com/Soil-Moisture-Sensor-Raspberry-Pi/
https://circuitdigest.com/microcontroller-projects/interfacing-pcf8591-adc-dac-module-with-raspberry-pi