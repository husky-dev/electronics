import network
from machine import Pin, ADC, deepsleep
from time import sleep, sleep_ms
import urequests as requests

device_id = 'groweresp32001'
api_token = 'pqtVNgjJzqGdUu3sngrZMxgN'
# deepsleep_sec = 60 * 1000 # 1 minute
deepsleep_sec = 10 * 60 * 1000 # 10 minutes

# Log

def log(msg):
  print('[-]: %s' % msg)

# Wlan

wlan = network.WLAN(network.STA_IF)

def wifi_connect(ssid = 'ASUS_D8', pswd = '08081987'):
  wlan.active(True)
  if not wlan.isconnected():
    log('connecting to network...')
    wlan.connect(ssid, pswd)
    while not wlan.isconnected():
      pass
  print('network config:', wlan.ifconfig())

def wifi_is_connected():
  return wlan.isconnected()

def wifi_disconnect():
  log('wifi disconnecting')
  wlan.disconnect()

# Power

def go_sleep():
  # Reduce power consuption by turning off internal pull resistors
  p1 = Pin(4, Pin.IN, Pin.PULL_HOLD)
  log('going to deepsleep for %d sec' % deepsleep_sec)
  deepsleep(deepsleep_sec)

# Sensors

humidity_sensor_enable = Pin(22, Pin.OUT, value = 0)
humidity_sensor_adc = ADC(Pin(32))
humidity_sensor_adc.atten(ADC.ATTN_11DB)
humidity_sensor_adc.width(ADC.WIDTH_9BIT)

def read_humidity():
  min = 156 # water
  max = 422 # air
  humidity_sensor_enable.on()
  sleep_ms(100)
  val = humidity_sensor_adc.read()
  humidity_sensor_enable.off()
  log('humidity sensor val=%d' % val)
  if val <= min: # water
    return 100.0
  if val >= max: # air
    return 0.0
  return 100 - ((val - min) / (max-min)) * 100

# Led

led = Pin(16, Pin.OUT, value = 1)

def blink():
  led.off()
  sleep_ms(300)
  led.on()

# Data

def send_log_event(data):
  url = 'https://api.smartapp.dev/iot/devices/%s/events/log' % device_id
  log('send log event, url=%s, data=%s' % (url, data))
  requests.post(url = url, headers = {'Authorization': api_token}, data = data)
  log('send log event done')

def process():
  log('process')
  log('connect to network')
  wifi_connect()
  log('connect to network done')
  log('read humidity')
  humidity = read_humidity()
  log('read humidity done, humidity=%f' % humidity)
  log('send data')
  send_log_event('{"humidity":%f}' % humidity)
  log('send data done')
  wifi_disconnect()
  blink()


# Main

def start():
  log('starting')
  while True:
    process()
    go_sleep()

start()
