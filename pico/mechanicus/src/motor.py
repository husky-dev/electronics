from machine import Pin, PWM, Timer

# L9110S
class Motor:
  def __init__(self, ia_pin, ib_pin, smoothnes = 200):
    self._smoothnes = smoothnes / 10 # cos timer is calling each 10ms
    self._IA_Pin = Pin(ia_pin, Pin.OUT)
    self._IA_PWM = PWM(self._IA_Pin)
    self._IA_PWM.freq(20000) # 20kHz
    self._IA_PWM.duty_u16(0)
    self._IB_Pin = Pin(ib_pin, Pin.OUT)
    self._IB_Pin.off()

    self._cur_speed = 0
    self._desired_speed = 0
    self._speed_change_step = 0
    self._timer = Timer()
    self._timer.init(mode=Timer.PERIODIC, period = 10, callback = self._udpate_speed)

  def stop(self):
    self.set_speed(0)

  def forward(self, speed = 100):
    self._IB_Pin.value(0)
    self.set_speed(speed)

  def back(self, speed = 100):
    self._IB_Pin.value(1)
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
    if self._IB_Pin.value() == 0:
      # Going forward
      self._IA_PWM.duty_u16(round(65535 / 100 * val))
    else:
      # Going back
      self._IA_PWM.duty_u16(65535 - round(65535 / 100 * val))

  # Return 0% - 100%
  def _get_pwm_speed(self):
    val = 0
    if self._IB_Pin.value() == 0:
      # Going forward
      val = round(self._IA_PWM.duty_u16() * 100 / 65535)
    else:
      # Going back
      val = round(100 - (self._IA_PWM.duty_u16() * 100 / 65535))
    if val < 0:
      val = 0
    elif val > 100:
      val = 100
    return val