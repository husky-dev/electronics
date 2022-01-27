from ps2 import PS2Controller
from motor_pwm import Motor
from time import sleep_ms
from led import RGBLed

motor_l = Motor(a_pin_no = 2, b_pin_no = 3)
motor_r = Motor(a_pin_no = 4, b_pin_no = 5)

# Green - data (di_pin_no)
# Orange - CMD (do_pin_no)
# Yellow - attn (cs_pin_no)
# Blue - CLK (clk_pin_no)
ps2ctl = PS2Controller(di_pin_no=6, do_pin_no=7, cs_pin_no=8, clk_pin_no=9)
led = RGBLed(r_pin_no=12, g_pin_no=11, b_pin_no=10)

# Log

def debug(val):
  print("[-][main]:", val)

def trace(val):
  return
  # print("[*][main]:", val)

def info(val):
  print("[+][main]:", val)

def warn(val):
  print("[!][main]:", val)

def err(val):
  print("[!][main]:", val)

# Motor

def stop():
  debug('stop')
  motor_l.stop()
  motor_r.stop()
  led.off()

def forward():
  debug('forward')
  motor_l.forward()
  motor_r.forward()
  led.green()

def reverse():
  debug('reverse')
  motor_l.reverse()
  motor_r.reverse()
  led.red()

def start():
  stop()
  info('start')
  info('waiting 1000 ms to PS2 controller start')
  sleep_ms(1000)
  info('start processing PS2 controller')
  ps2ctl.init()
  while True:
    ps2ctl.read()
    if ps2ctl.available:
      if ps2ctl.ly < 0:
        forward()
      elif ps2ctl.ly > 0:
        reverse()
      else:
        stop()
    else:
      led.blink(color = "blue")
    sleep_ms(50)

start()
