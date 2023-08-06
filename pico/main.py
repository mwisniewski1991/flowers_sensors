import network
import gc
import urequests
import utime as time
from machine import Pin, ADC
from dht import DHT11
from config import NETWORK_NAME, NETWORK_PASS, API_URL

gc.enable()
gc.collect()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(NETWORK_NAME, NETWORK_PASS)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0] )
    print('-------------------------------')


LED_PIN_NUMBER = 14
DHT_PIN_NUMBER = 28

led = Pin(LED_PIN_NUMBER, Pin.OUT)
adc = ADC(26)
conversion_factor = 100 / (65535)

while True:
    time.sleep(10)

    led.toggle()
    moisture = 130 - (adc.read_u16() * conversion_factor)

    try:
        pin = Pin(DHT_PIN_NUMBER, Pin.OUT, Pin.PULL_DOWN)
        sensor = DHT11(pin)
        temperature = sensor.temperature
        humidity = sensor.humidity

    except:
        print("ERROR FOR SENSOR")
        temperature = -1.0
        humidity = -1.0
        
    url = API_URL + "?id=1234&name=flower_1&temeprature=" + str(temperature) + "&soil_moisture=" + str(moisture) + "&humidity=" + str(humidity) 

    # print("-------------------------------")
    # print("Moisture: {}".format(moisture))
    # print("Temperature: {}".format(temperature))
    # print("Humidity: {}".format(humidity))
    
    # print(url)
    r = urequests.get(url)
    print(r.json())
    r.close()