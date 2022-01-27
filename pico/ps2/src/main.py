from ps2 import PS2Controller
import time

# Green - data (di_pin_no)
# Orange - CMD (do_pin_no)
# Yellow - attn (cs_pin_no)
# Blue - CLK (clk_pin_no)
ctl = PS2Controller(di_pin_no=7, do_pin_no=8, cs_pin_no=9, clk_pin_no=10)

ctl.init()
while True:
  buff = ctl.read_once()
  print(ctl.lx, ctl.ly, ctl.rx, ctl.ry)
  print(ctl.pressed_keys)
  time.sleep_ms(50)
