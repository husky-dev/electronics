import network
from machine import Pin, ADC, I2C
from time import sleep
import dht
import bh1750fvi
import ssd1306

# Wlan

def wlan_connect(ssid = 'ASUS_D8', pswd = '08081987'):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, pswd)
    while not wlan.isconnected():
      pass
  print('network config:', wlan.ifconfig())

def wifi_is_connected():
  return wlan.isconnected()

# Humidity

# Return humidity in procents
# 0 - air
# 100 - water
def get_ground_humidity(pin = 34):
  adc = ADC(Pin(pin))
  adc.atten(ADC.ATTN_11DB)
  adc.width(ADC.WIDTH_9BIT)
  min = 156 # water
  max = 422 # air
  val = adc.read()
  if val <= min: # water
    return 100.0
  if val >= max: # air
    return 0.0
  return 100 - ((val - min) / (max-min)) * 100

# Temperature

def get_air_data(pin = 25):
  d = dht.DHT22(Pin(pin))
  d.measure()
  return { "temperature": d.temperature(), "humidity": d.humidity() }

# Ligth

light_sensor_i2c = I2C(scl=Pin(26), sda=Pin(27))

def get_light_data():
  return bh1750fvi.sample(light_sensor_i2c)

# Display

display_i2c = I2C(-1, scl=Pin(4), sda=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, display_i2c)
display.contrast(100)

# Led
green_led = Pin(14, Pin.OUT)

# Main

def start():
  while True:
    loop()
    sleep(5)


def loop():
  print("[+]: loop")
  display.fill(0)

  light = get_light_data()
  print("[-]: light=", light)
  display.text("Light: %.2f" % light, 0, 0)

  humidity = get_ground_humidity()
  print("[-]: humidity=", humidity)
  display.text("Humid: %.2f%%" % humidity, 0, 12)

  air = get_air_data()
  print("[-]: air=", air)
  display.text("Tempr: %.2fC" % air["temperature"], 0, 24)

  display.show()
  print("[+]: loop done")

  # green_led.on()
  # sleep(1)
  # green_led.off()
