"""
# CSN-A2 Thermal printer

- https://www.adafruit.com/product/597
- https://learn.adafruit.com/mini-thermal-receipt-printer
- https://github.com/adafruit/Adafruit-Thermal-Printer-Library/blob/master/Adafruit_Thermal.cpp

## Requirements:

- UART baudrate: 19200
- Requires 5-9VDC @ 1.5Amp power supply during print

## Connection example:

from machine import Pin, UART
uart = UART(1, baudrate=19200, tx=Pin(4), rx=Pin(5))
"""

# ASCII codes used by some of the printer config commands:

ASCII_TAB = '\t' # Horizontal tab
ASCII_LF = '\n'  # Line feed
ASCII_FF = '\f'  # Form feed
ASCII_CR = '\r'  # Carriage return
ASCII_DC2 = 18   # Device control 2
ASCII_ESC = 27   # Escape
ASCII_FS = 28    # Field separator
ASCII_GS = 29    # Group separator

# Character commands

FONT_MASK = (1 << 0)          # Select character font A or B
INVERSE_MASK = (1 << 1)       # Turn on/off white/black reverse printing mode.
UPDOWN_MASK = (1 << 2)        # Turn on/off upside-down printing mode
BOLD_MASK = (1 << 3)          # Turn on/off bold printing mode
DOUBLE_HEIGHT_MASK = (1 << 4) # Turn on/off double-height printing mode
DOUBLE_WIDTH_MASK = (1 << 5)  # Turn on/off double-width printing mode
STRIKE_MASK = (1 << 6)        # Turn on/off deleteline mode

# Internal character sets used with ESC R n

CHARSET_USA = 0 # American character set
CHARSET_FRANCE = 1 # French character set
CHARSET_GERMANY = 2 # German character set
CHARSET_UK = 3 # UK character set
CHARSET_DENMARK1 = 4 # Danish character set 1
CHARSET_SWEDEN = 5 # Swedish character set
CHARSET_ITALY = 6 # Italian character set
CHARSET_SPAIN1 = 7 # Spanish character set 1
CHARSET_JAPAN = 8 # Japanese character set
CHARSET_NORWAY = 9 # Norwegian character set
CHARSET_DENMARK2 = 10 # Danish character set 2
CHARSET_SPAIN2 = 11 # Spanish character set 2
CHARSET_LATINAMERICA = 12 # Latin American character set
CHARSET_KOREA = 13 # Korean character set
CHARSET_SLOVENIA = 14 # Slovenian character set
CHARSET_CROATIA = 14 # Croatian character set
CHARSET_CHINA = 15 # Chinese character set

# Character code tables used with ESC t n

CODEPAGE_CP437 = 0 # USA, Standard Europe character code table
CODEPAGE_KATAKANA = 1 # Katakana (Japanese) character code table
CODEPAGE_CP850 = 2 # Multilingual character code table
CODEPAGE_CP860 = 3 # Portuguese character code table
CODEPAGE_CP863 = 4 # Canadian-French character code table
CODEPAGE_CP865 = 5 # Nordic character code table
CODEPAGE_WCP1251 = 6 # Cyrillic character code table
CODEPAGE_CP866 = 7 # Cyrillic #2 character code table
CODEPAGE_MIK = 8 # Cyrillic/Bulgarian character code table
CODEPAGE_CP755 = 9 # East Europe, Latvian 2 character code table
CODEPAGE_IRAN = 10 # Iran 1 character code table
CODEPAGE_CP862 = 15 # Hebrew character code table
CODEPAGE_WCP1252 = 16 # Latin 1 character code table
CODEPAGE_WCP1253 = 17 # Greek character code table
CODEPAGE_CP852 = 18 # Latin 2 character code table
CODEPAGE_CP858 = 19 # Multilingual Latin 1 + Euro character code table
CODEPAGE_IRAN2 = 20 # Iran 2 character code table
CODEPAGE_LATVIAN = 21 # Latvian character code table
CODEPAGE_CP864 = 22 # Arabic character code table
CODEPAGE_ISO_8859_1 = 23 # West Europe character code table
CODEPAGE_CP737 = 24 # Greek character code table
CODEPAGE_WCP1257 = 25 # Baltic character code table
CODEPAGE_THAI = 26 # Thai character code table
CODEPAGE_CP720 = 27 # Arabic character code table
CODEPAGE_CP855 = 28 # Cyrillic character code table
CODEPAGE_CP857 = 29 # Turkish character code table
CODEPAGE_WCP1250 = 30 # Central Europe character code table
CODEPAGE_CP775 = 31 # Baltic character code table
CODEPAGE_WCP1254 = 32 # Turkish character code table
CODEPAGE_WCP1255 = 33 # Hebrew character code table
CODEPAGE_WCP1256 = 34 # Arabic character code table
CODEPAGE_WCP1258 = 35 # Vietnam character code table
CODEPAGE_ISO_8859_2 = 36 # Latin 2 character code table
CODEPAGE_ISO_8859_3 = 37 # Latin 3 character code table
CODEPAGE_ISO_8859_4 = 38 # Baltic character code table
CODEPAGE_ISO_8859_5 = 39 # Cyrillic character code table
CODEPAGE_ISO_8859_6 = 40 # Arabic character code table
CODEPAGE_ISO_8859_7 = 41 # Greek character code table
CODEPAGE_ISO_8859_8 = 42 # Hebrew character code table
CODEPAGE_ISO_8859_9 = 43 # Turkish character code table
CODEPAGE_ISO_8859_15 = 44 # Latin 3 character code table
CODEPAGE_THAI2 = 45 # Thai 2 character code page
CODEPAGE_CP856 = 46 # Hebrew character code page
CODEPAGE_CP874 = 47 # Thai character code page


class Thermal_Printer:
  def __init__(self, uart):
    self._uart = uart
    self._print_mode = 0

  def print(self, msg):
    self._uart.write(msg)

  def println(self, msg):
    self._uart.write('%s\n' % msg)

  def ln(self):
    self._uart.write('\n')

  def dln(self):
    self._uart.write('\n\n')

  def normal(self):
    self._print_mode = 0
    self.write_print_mode()

  # Value: L - left, C - center, R - right
  def justify(self, value):
    value = value.upper()
    pos = 0
    if value is 'L':
      pos = 0
    if value is 'C':
      pos = 1
    if value is 'R':
      pos = 2
    self.write_bytes(ASCII_ESC, 'a', pos)

  # Value: S - small, M - middle, L - large
  def set_size(self, value):
    value = value.upper()
    if value is 'M':
      self.double_height_on()
      self.double_width_off()
    elif value is 'L':
      self.double_height_on()
      self.double_width_on()
    else:
      self.double_width_off()
      self.double_height_off()

  # Value: A - first, B - second
  def set_font(self, value):
    value = value.upper()
    if value is 'A':
      self.unset_print_mode(FONT_MASK)
    else:
      self.set_print_mode(FONT_MASK)

  def double_height_on(self):
    self.set_print_mode(DOUBLE_HEIGHT_MASK)

  def double_height_off(self):
    self.unset_print_mode(DOUBLE_HEIGHT_MASK)

  def double_width_on(self):
    self.set_print_mode(DOUBLE_WIDTH_MASK)

  def double_width_off(self):
    self.unset_print_mode(DOUBLE_WIDTH_MASK)

  def strike_on(self):
    self.set_print_mode(STRIKE_MASK)

  def strike_off(self):
    self.unset_print_mode(STRIKE_MASK)

  def bold_on(self):
    self.set_print_mode(BOLD_MASK)

  def bold_off(self):
    self.unset_print_mode(BOLD_MASK)

  def inverse_on(self):
    # firmware >= 268
    self.write_bytes(ASCII_GS, 'B', 1)

  def inverse_off(self):
    # firmware >= 268
    self.write_bytes(ASCII_GS, 'B', 0)

  def upside_down_on(self):
    self.write_bytes(ASCII_ESC, '{', 1)

  def upside_down_off(self):
    # firmware >= 268
    self.write_bytes(ASCII_ESC, '{', 0)

  def feed(self, lines):
    # firmware >= 264
    self.write_bytes(ASCII_ESC, 'd', lines)

  def flush(self):
    self.write_bytes(ASCII_FF)

  def set_print_mode(self, mask):
    self._print_mode |= mask
    self.write_print_mode()

  def unset_print_mode(self, mask):
    self._print_mode &= (~mask) & 0xFF
    self.write_print_mode()

  def write_print_mode(self):
    # print("{0:b}".format(self._print_mode))
    self.write_bytes(ASCII_ESC, '!', self._print_mode)

  """
  Underlines of different weights can be produced:
  0 - no underline
  1 - normal underline
  2 - thick underline
  """
  def underline_on(self, weight = 2):
    if weight > 2: weight = 2
    self.write_bytes(ASCII_ESC, '-', weight)

  def underline_off(self):
    self.write_bytes(ASCII_ESC, '-', 0)

  def set_char_spacing(self, spacing):
    self.write_bytes(ASCII_ESC, ' ', spacing)

  # def has_paper(self):
    # self.write_bytes(ASCII_ESC, 'v', 0)
    # self.write_bytes(ASCII_GS, 'r', 0)
    # data = self._uart.read()

  def set_barcode_height(self, val):
    if (val < 1):
      val = 1
    self.write_bytes(ASCII_GS, 'h', val)

  def set_code_page(self, val = 0):
    """
    Selects alt symbols for 'upper' ASCII values 0x80-0xFF

    :param str val: Value of the desired character code page
    """
    if val > 47:
      val = 47
    self.write_bytes(ASCII_ESC, 't', val)

  def write_bytes(self, *items):
    arr = []
    for item in items:
      if type(item) is str:
        arr.append(ord(item[0]))
      else:
        arr.append(item)
    self._uart.write(bytes(arr))
