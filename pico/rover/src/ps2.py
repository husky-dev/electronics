import time
from machine import Pin

class PS2Controller:
  # These are our button constants
  SELECT = 1
  L3 = 2
  R3 = 3
  START = 4
  UP = 5
  RIGHT = 6
  DOWN = 7
  LEFT = 8
  L2 = 9
  R2 = 10
  L1 = 11
  R1 = 12
  TRIANGLE = 13
  CIRCLE = 14
  CROSS = 15
  SQUARE = 16
  KEYS = dict([
    (SELECT, "SELECT"),
    (L3, "L3"),
    (R3, "R3"),
    (START, "START"),
    (UP, "UP"),
    (RIGHT, "RIGHT"),
    (DOWN, "DOWN"),
    (LEFT, "LEFT"),
    (L2, "L2"),
    (R2, "R2"),
    (L1, "L1"),
    (R1, "R1"),
    (TRIANGLE, "TRIANGLE"),
    (CIRCLE, "CIRCLE"),
    (CROSS, "CROSS"),
    (SQUARE, "SQUARE"),
  ])

  CTRL_CLK = 10
  CTRL_BYTE_DELAY = 16

  CMD_SHORT_POLL = [0x01, 0x42, 0x00, 0x00, 0x00]
  CMD_ENTER_CONFIG = [0x01, 0x43, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
  CMD_SET_MODE = [0X01, 0x44, 0x00,
          0x01, # 00 normal; 01 red or analog
          0x03, # 03 lock; ee no lock
          0x00, 0x00, 0x00, 0x00]
  CMD_SET_BYTES_LARGE = [0x01, 0x4F, 0x00, 0xFF, 0xFF, 0x03, 0x00, 0x00, 0x00]
  CMD_EXIT_CONFIG = [0x01, 0x43, 0x00, 0x00, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A]
  CMD_ENABLE_RUMBLE = [0x01, 0x4D, 0x00, 0x00, 0x01]
  CMD_TYPE_READ = [0x01, 0x45, 0x00, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A]
  CMD_READ_DATA = [0X01, 0X42, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00, 0X00]

  MAX_READ_DELAY = 1500

  VALID_MODES = [0X41, 0X73]

  def __init__(self, di_pin_no=13, do_pin_no=12, cs_pin_no=15, clk_pin_no=14):
    self.di_pin_no = di_pin_no
    self.do_pin_no = do_pin_no
    self.cs_pin_no = cs_pin_no
    self.clk_pin_no = clk_pin_no

    self.di = Pin(self.di_pin_no, Pin.IN, Pin.PULL_UP) # DI = DAT
    self.do = Pin(self.do_pin_no, Pin.OUT) # DO = CMD
    self.cs = Pin(self.cs_pin_no, Pin.OUT)
    self.clk = Pin(self.clk_pin_no, Pin.OUT)

    self.buff_out = [0x01, 0x42]
    self.buff_in = [0] * 9
    self.pressed_keys = []
    self.read_delay = 1
    self.last_read_ms = 0
    self.available = False

    self.rx = 0
    self.ry = 0
    self.lx = 0
    self.ly = 0

  @property
  def red_mode(self): # analog mode
    return self.buff_in[1] & 0xf0 == 0x70

  def do_h(self):
    self.do.value(1)

  def do_l(self):
    self.do.value(0)

  def cs_h(self):
    self.cs.value(1)

  def cs_l(self):
    self.cs.value(0)

  def clk_h(self):
    self.clk.value(1)

  def clk_l(self):
    self.clk.value(0)

  def debug(self, val):
    print("[-][PS2]:", val)

  def trace(self, val):
    return
    # print("[*][PS2]:", val)

  def info(self, val):
    print("[+][PS2]:", val)

  def warn(self, val):
    print("[!][PS2]:", val)

  def err(self, val):
    print("[!][PS2]:", val)

  # noinspection PyUnresolvedReferences
  def delay_byte(self):
    time.sleep_us(self.read_delay)

  # noinspection PyUnresolvedReferences
  def delay_clk(self):
    time.sleep_us(self.CTRL_CLK)

  # noinspection PyUnresolvedReferences
  def delay_read(self):
    time.sleep_us(self.CTRL_BYTE_DELAY)
    # time.sleep_ms(self.read_delay)

  def cmd(self, cmd):
    ret = 0
    for i in range(8):
      if cmd & 1 << i:
        self.do_h()
      else:
        self.do_l()
      self.clk_l()
      self.delay_clk()
      if self.di.value():
        ret |= 1 << i
      self.clk_h()
    self.do_h()
    self.delay_byte()
    return ret

  def cmd_group(self, cmds):
    self.cs_l()
    self.delay_byte()
    for cmd in cmds:
      self.cmd(cmd)
    self.cs_h()
    self.delay_read()

  def init(self):
    self.info("init")
    self.do_h()
    self.clk_h()
    
    # new error checking. First, read gamepad a few times to see if it's talking
    self.read()
    self.read()
    # see if it talked - see if mode came back. 
    # If still anything but 41, 73 or 79, then it's not talking
    if self.buff_in[1] not in self.VALID_MODES:
      self.err("controller mode not matched or no controller found, expected 0x41, 0x42, 0x73 or 0x79, but got {:02x}".format(self.buff_in[1]))
      # return error code 1
      return 1

    self.debug("control type: {:02x}".format(self.buff_in[1]))
    # try setting mode, increasing delays if need be.
    self.read_delay = 1

    for i in range(10):
      # start config run
      self.cmd_group(self.CMD_ENTER_CONFIG)

      # read type
      self.delay_byte()
      self.do_h()
      self.clk_h()
      self.cs_l()
      self.delay_byte()

      #
      temp = [0] * len(self.CMD_TYPE_READ)
      for j in range(9):
        for cmd in self.CMD_TYPE_READ:
          temp[j] = self.cmd(cmd)
      self.cs_h()

      self.cmd_group(self.CMD_SET_MODE)
      # self.cmd_group(self.CMD_ENABLE_RUMBLE)
      self.cmd_group(self.CMD_EXIT_CONFIG)
      self.read()
      if self.buff_in[1] in self.VALID_MODES:
        self.debug("read_delay configed: {}".format(self.read_delay))
        break
      else:
        self.read_delay += 1
        self.debug("read_delay++: {}".format(self.read_delay))

  def read(self):
    self.trace("read once")
    now = time.ticks_ms()
    delay = now - self.last_read_ms
    if delay > self.MAX_READ_DELAY:
      self.debug("delay bigger then MAX_READ_DELAY, now: {}, last_read_ms: {}, delay: {}".format(now, self.last_read_ms, delay))
      self.reconfig()
    elif delay < self.read_delay:
      # noinspection PyUnresolvedReferences
      self.debug("waiting for {} ms".format(self.read_delay - delay))
      time.sleep_ms(self.read_delay - delay)

    self.buff_in = [0] * 9
    self.pressed_keys.clear()

    for j in range(5):
      self.do_h()
      self.clk_h()
      self.cs_l()
      self.delay_byte()

      for i, c in enumerate(self.CMD_READ_DATA):
        self.buff_in[i] = self.cmd(c)

      self.cs_h()

      if self.buff_in[1] in self.VALID_MODES:
        if not self.available:
          self.info('available')
        self.available = True
        self.trace("valid mode: {:08b}".format(self.buff_in[1]))
        break
      else:
        if self.available:
          self.info('not available')
        self.available = False
        self.trace("invalid mode: {:08b}, retry: {}, delay: {}".format(self.buff_in[1], j, self.read_delay))
        self.reconfig()
        self.delay_read()

    if self.buff_in[1] not in self.VALID_MODES and self.read_delay < 10:
      self.read_delay += 1

    self.last_read_ms = time.ticks_ms()
    self.process_buff_in()

    return self.buff_in

  def reconfig(self):
    self.trace("reconfig")
    self.cmd_group(self.CMD_ENTER_CONFIG)
    self.cmd_group(self.CMD_SET_MODE)
    self.cmd_group(self.CMD_EXIT_CONFIG)

  def process_buff_in(self):
    self.trace("pocessing buff_in")
    for d in self.buff_in:
      self.trace("{:08b}".format(d))

    key_raw = (self.buff_in[4] << 8) | self.buff_in[3]
    for i in range(1, 17):
      if not key_raw & 1 << i - 1:
        self.pressed_keys.append(i)

    if self.red_mode:
      self.rx = self.buff_in[5] - 128
      self.ry = self.buff_in[6] - 128
      self.lx = self.buff_in[7] - 128
      self.ly = self.buff_in[8] - 128
    if self.pressed_keys:
      out = "keys:" + ','.join(self.KEYS[k] for k in self.pressed_keys) + "; "
    else:
      out = ""
    if self.red_mode and (out or any(x != 0 for x in [self.rx, self.ry, self.lx, self.ly])):
      out += "pos: (lx,ly):{},{}; (rx,ry): {},{}".format(self.lx, self.ly, self.rx, self.ry)

    if out:
      self.debug(out)

  def run(self):
    self.init()
    while True:
      self.read()
      time.sleep_ms(50)
