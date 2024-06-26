# PiPicoWx
Simple rest api and webpage for Raspberry Pi Pico W using micropython-phew library and DHT11 sensor

Developed for micropython use with Raspberry Pi Pico W.


Most examples of using the DHT11 sensor show a sort of repeating call or reporting from the sensor.  I wanted something that
I could just call on demand, for a robot I'm working on, via an API call.  I couldn't find the precise answer although there were
other tutorials on using the micropython-phew library to set up a simple rest API.

The point of this program is to provide a simple API endpoint, and also a simple web page endpoint to poll the DHT11 sensor hooked to 
a Raspberry Pi Pico W running on one's local network.

Ensure the following packages and scripts/drivers are loaded in your Pi Pico W:
dht11.py from https://pypi.org/project/dht11/
micro-python phew from Pimoroni: https://pypi.org/project/micropython-phew/ or from here: https://github.com/pimoroni/phew

Pinouts used on my Pi Pico W, but you can decide on your pinouts (actual pin numbers unless specifed as GP Pin):
 - Power - pin 39 - VSYS
 - Ground - pin 38 - GND
 - DHT11 data - pin 4 - GP2

Ensure GP2 data pin is set as Pin.OUT and Pin.PULL_DOWN

The program will start a server with an API endpoint runing at /data and also one can call the webpage with just the ip the server is running on, press the buttonm, and poll the sensor.
WxStationApiTest.py is included here as a simple test call to the /data endpoint to illustrate how this can be used on your local network by other programs.  Be sure to replace the url in the program with the url/ip address provided by YOUR raspberry pi Pico W!  Be sure to fill in YOUR SSID and password for YOUR local network in the main program.

![IMG_9639](https://github.com/DutchBoy65/PiPicoWx/assets/133307895/13dca4ef-190c-429e-873b-7b48cbf1422a)
