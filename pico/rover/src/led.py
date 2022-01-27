from machine import Pin
from time import sleep_ms

class RGBLed:
  def __init__(self, r_pin_no, g_pin_no, b_pin_no):
    self._r_pin = Pin(r_pin_no, Pin.OUT, 0)
    self._g_pin = Pin(g_pin_no, Pin.OUT, 0)
    self._b_pin = Pin(b_pin_no, Pin.OUT, 0)

  def red_on(self):
    self._r_pin.on()

  def red_off(self):
    self._r_pin.off()

  def green_on(self):
    self._g_pin.on()

  def green_off(self):
    self._g_pin.off()

  def blue_on(self):
    self._b_pin.on()

  def blue_off(self):
    self._b_pin.off()

  def off(self):
    self.red_off()
    self.green_off()
    self.blue_off()

  def red(self):
    self.off()
    self.red_on()

  def green(self):
    self.off()
    self.green_on()
  
  def blue(self):
    self.off()
    self.blue_on()

  def blink(self, color = "green", delay_ms = 100):
    self.off()
    if color == "red":
      self.red_on()
    if color == "green":
      self.green_on()
    if color == "blue":
      self.blue_on()
    sleep_ms(delay_ms)
    self.off()
    sleep_ms(delay_ms)
