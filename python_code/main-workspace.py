import machine
import dht
from soil_check import check_soil
import network
import json

# WiFi configuration
WIFI_SSID = "Your_WiFi_SSID"
WIFI_PASSWORD = "Your_WiFi_Password"

# MQTT configuration
MQTT_BROKER = "Your_MQTT_Broker_IP_or_Hostname"
MQTT_PORT = 1883  # Default MQTT port
MQTT_TOPIC = "veggers"
MQTT_CLIENT_ID = "esp8266_client"


# Define data pin for ESP8266
SOIL_PIN = 0
DATA_PIN = 2

# Setup Soil and temp sensors
soil_pin = machine.ADC(machine.Pin(SOIL_PIN)))
sensors = dht.DHT11(machine.Pin(DATA_PIN))

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('WiFi connected:', sta_if.ifconfig())

def read_soil_moisture():
    #Read analog value
    soil_val = soil_pin.read()
    soil_moisture = (soil_value - 0) * 100 / (1023 - 0)
    return soil_moisture

def check_temperature():
    try:
        # Read Temperature
        sensors.measure()
        temp = sensors.temperature()
        humidity = sensors.humidity()

        return temp, humidity
    except OSError as ex:
        print("Failed to read")
        return None, None

def main():
    connect_wifi()
    ## Main Loop to read temperature
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    client.connect()
    
    while True:
        # Read soil moisture
        moisture = read_soil_moisture()
        print(f"Soil Moisture: {moisture:.2f}%")
    
        # Read temperature and humidity
        temp, humidity = check_temperature()
        if temp is not None and humidity is not None:
            print(f'Temperature: {temp} C, humidity: {humidity}')
            data = {
                    "soil_moisture": round(moisture, 2),
                    "temperature": temp,
                    "humidity": humidity
                }
                message = json.dumps(data)
                client.publish(MQTT_TOPIC, message)
                print(f"Published: {message}")
        else:
            print('Sensor reading failed')
    
        # sleep for next reading
        time.sleep(5)

if __name__ == "__main__":
    main()
