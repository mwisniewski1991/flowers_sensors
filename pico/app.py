from machine import Pin, ADC
import utime as time
from dht import DHT11

LED_PIN_NUMBER = Pin(14, Pin.OUT)
DHT_PIN_NUMBER = 28
adc = ADC(26)
conversion_factor = 100 / (65535)

while True:
    time.sleep(2.5)

    LED_PIN_NUMBER.toggle()

    pin = Pin(DHT_PIN_NUMBER, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)

    moisture = 130 - (adc.read_u16() * conversion_factor)
    temperature = sensor.temperature
    humidity = sensor.humidity

    print("-------------------------------")
    print("Moisture: {}".format(moisture))
    print("Temperature: {}".format(temperature))
    print("Humidity: {}".format(humidity))
    