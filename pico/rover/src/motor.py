from machine import PWM, Timer, Pin

class Motor:
  def __init__(self, ia_pin_no, ib_pin_no):
    self._ia_pin = Pin(ia_pin_no, Pin.OUT, 0)
    self._ib_pin = Pin(ib_pin_no, Pin.OUT, 0)

  def stop(self):
    self._ia_pin.off()
    self._ib_pin.off()

  def forward(self):
    self._ia_pin.high()
    self._ib_pin.off()

  def reverse(self):
    self._ia_pin.off()
    self._ib_pin.high()
