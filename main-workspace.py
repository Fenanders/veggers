import machine
import dht
from soil_check import check_soil

# Define data pin for ESP8266
DATA_PIN = 2

sensors = dht.DHT11(machine.Pin(DATA_PIN))


def check_temperature():
    try:
        sensors.measure()
        temp = sensors.temperature()
        humidity = sensors.humidity()

        return temp, humidity
    except OSError as ex:
        print("Failed to read")
        return None, None

## Main Loop to read temperature
while True:
    temp, humidity = check_temperature()
    if temp is not None and humidity is not None:
        print(f'Temperature: {temp} C, humidity: {humidity}')
    else:
        print('Sensor reading failed')
