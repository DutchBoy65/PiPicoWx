# PiPicoWx - a simple rest api and web page interface for a local network weather station with a DHT11 sensor
# PiPicoWx uses the micropython-phew library for a simple setup of a webserver with a /data endpoint to call from another program
# A simple webpage with a button is also provided so that one can get the readings from a weblink

import network
import time
import json
from machine import Pin
import dht
from phew import server, logging

# Connect to your Wi-Fi network
ssid = 'your_ssid'
password = 'your_password'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

# Get the IP address
ip = connect()

# Initialize the DHT11 sensor
dht_sensor = dht.DHT11(Pin(2, Pin.OUT, Pin.PULL_DOWN))  # Adjust the pin number as needed

def read_dht11():
    for i in range(5):  # Retry up to 5 times
        try:
            print("Measuring...")
            dht_sensor.measure()
            print("Measure complete")
            temp = dht_sensor.temperature  # Correct property access without parentheses
            print(f"Temperature method call: {temp}")
            humid = dht_sensor.humidity    # Correct property access without parentheses
            print(f"Humidity method call: {humid}")
            return temp, humid
        except Exception as e:
            logging.error(f"Error reading sensor on attempt {i + 1}: {e}")
            time.sleep(2)  # Delay before retrying
    raise Exception("Failed to read sensor after multiple attempts")

# Define the endpoint to serve the data
@server.route("/data")
def data(request):
    try:
        temp, humid = read_dht11()
        response = {
            'temperature': temp,
            'humidity': humid
        }
        return json.dumps(response), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logging.error(f"Final error reading sensor: {e}")
        return json.dumps({'error': 'Failed to read sensor data'}), 500, {'Content-Type': 'application/json'}

# Serve the HTML page with a button to request data
@server.route("/")
def index(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Indoor Weather Station</title>
        <script>
            async function getWeatherData() {
                try {
                    const response = await fetch('/data');
                    if (response.ok) {
                        const data = await response.json();
                        document.getElementById('result').innerText = `Temperature: ${data.temperature}°C, Humidity: ${data.humidity}%`;
                    } else {
                        document.getElementById('result').innerText = 'Failed to get data from the server';
                    }
                } catch (error) {
                    console.error('Error:', error);
                    document.getElementById('result').innerText = 'Error fetching data';
                }
            }
        </script>
    </head>
    <body>
        <h1>Indoor Weather Station</h1>
        <button onclick="getWeatherData()">Get Current Reading</button>
        <p id="result"></p>
    </body>
    </html>
    """
    return html_content, 200, {'Content-Type': 'text/html'}

# Start the server
print(f"Starting server on {ip}")
server.run(host="0.0.0.0", port=80)
