# Preasure, temperature, humidity

# from machine import I2C, Pin
# from BME280 import BME280

# bme280 = BME280(I2C(0, sda=Pin(0), scl=Pin(1), freq=100000))
# Returns: 
# {'preasure': 987.2784, 'humidity': 47.44043, 'temperature': 23.75}
# data = bme280.read_data()


# Dust detection

# from machine import Pin, UART
# from time import sleep
# from PMS3003 import PMS3003

# enable = Pin(18, Pin.OUT, value = 1)
# pms3003 = PMS3003(UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5)))
