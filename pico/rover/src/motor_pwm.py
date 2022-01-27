from machine import PWM, Timer, Pin

# L9110S
class Motor:
  def __init__(self, a_pin_no, b_pin_no, smoothnes = 200):
    self._smoothnes = smoothnes / 10 # cos timer is calling each 10ms
    self._a_pin_no = a_pin_no
    self._a_pwm = PWM(Pin(a_pin_no, Pin.OUT))
    self._a_pwm.freq(20000) # 20kHz
    self._a_pwm.duty_u16(0)
    
    self._b_pin_no = b_pin_no
    self._b_pin = Pin(b_pin_no, Pin.OUT)
    self._b_pin.off()

    self._cur_speed = 0
    self._desired_speed = 0
    self._speed_change_step = 0
    self._timer = Timer()
    self._timer.init(mode=Timer.PERIODIC, period = 10, callback = self._udpate_speed)

  def stop(self):
    self.set_speed(0)

  def forward(self, speed = 100):
    self._b_pin.value(0)
    self.set_speed(speed)

  def reverse(self, speed = 100):
    self._b_pin.value(1)
    self.set_speed(speed)

  def set_speed(self, val = 100):
    # In case if we have to change speed imidiatly
    if self._smoothnes == 0:
      self._set_pwm_speed(val)
    else:
      self._desired_speed = val
      self._speed_change_step = abs(val - self._cur_speed) / self._smoothnes

  def _udpate_speed(self, timer):
    if self._desired_speed == self._cur_speed: return
    # Speed up
    if self._desired_speed > self._cur_speed:
      val = self._cur_speed + self._speed_change_step
      if val > self._desired_speed:
        val = self._desired_speed
      # print('[-] spped up to: {:0.2f}, desierd: {:0.2f}'.format(val, self._desired_speed))
      self._set_pwm_speed(val)
    # Speed donw
    if self._desired_speed < self._cur_speed:
      val = self._cur_speed - self._speed_change_step
      if val < self._desired_speed:
        val = self._desired_speed
      # print('[-] spped down to: {:0.2f}, desierd: {:0.2f}'.format(val, self._desired_speed))
      self._set_pwm_speed(val)
    
  # Setting speed 0% - 100%
  def _set_pwm_speed(self, val = 100):
    if val > 100:
      val = 100
    elif val < 0:
      val = 0
    self._cur_speed = val
    if self._b_pin.value() == 0:
      # Going forward
      self._a_pwm.duty_u16(round(65535 / 100 * val))
    else:
      # Going back
      self._a_pwm.duty_u16(65535 - round(65535 / 100 * val))

  # Return 0% - 100%
  def _get_pwm_speed(self):
    val = 0
    if self._b_pin.value() == 0:
      # Going forward
      val = round(self._a_pwm.duty_u16() * 100 / 65535)
    else:
      # Going back
      val = round(100 - (self._a_pwm.duty_u16() * 100 / 65535))
    if val < 0:
      val = 0
    elif val > 100:
      val = 100
    return val