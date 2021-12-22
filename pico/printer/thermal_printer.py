"""
# CSN-A2 Thermal printer

The code on Adafruit Thermal Printer Library (https://github.com/adafruit/Adafruit-Thermal-Printer-Library)

Usefull links:
- https://www.adafruit.com/product/597
- https://learn.adafruit.com/mini-thermal-receipt-printer

## Requirements:

- UART baudrate: 19200
- Requires 5-9VDC @ 1.5Amp power supply during print

## Connection example:

from machine import Pin, UART
uart = UART(1, baudrate=19200, tx=Pin(4), rx=Pin(5))
"""

"""
Number of microseconds to issue one byte to the printer.  11 bits
(not 8) to accommodate idle, start and stop bits.  Idle time might
be unnecessary, but erring on side of caution here.
"""
from time import sleep_us, sleep_ms

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

symbols_map = {
  'І': 'I',
  'і': 'i',
  'Ї': chr(0xaf + 848),
  'ї': chr(0xbf + 848),
  'Є': chr(0xaa + 848),
  'є': chr(0xba + 848),
  'Ґ': chr(0xa5 + 848),
  'ґ': chr(0xb4 + 848),
  'Ë': chr(0xa8 + 848),
  'ё': chr(0xb8 + 848),
}

# Barcode types

UPC_A = 0   # UPC-A barcode system. 11-12 char */
UPC_E = 1   # UPC-E barcode system. 11-12 char */
EAN13 = 2   # EAN13 (JAN13) barcode system. 12-13 char */
EAN8 = 3    # EAN8 (JAN8) barcode system. 7-8 char */
CODE39 = 4  # CODE39 barcode system. 1<=num of chars */
ITF = 5     # ITF barcode system. 1<=num of chars, must be an even number */
CODABAR = 6 # CODABAR barcode system. 1<=num<=255 */
CODE93 = 7  # CODE93 barcode system. 1<=num<=255 */
CODE128 = 8 # CODE128 barcode system. 2<=num<=255 */

class Thermal_Printer:
  def __init__(self, uart, firmware = 268):
    self._uart = uart
    self._print_mode = 0
    # Time to print a single dot line, in microseconds
    self._dot_print_time = 30000 # 30ms
    # Time to feed a single dot line, in microseconds
    self._dot_feed_time = 2100 #2.1ms
    self._char_height = 24
    self._line_spacing = 6
    self._column = 0
    self._max_column = 32
    self._barcode_height = 50
    self._firmware = firmware
    self._cur_code_page = 0
    self._max_chunk_height = 255

  """
  Sets print and feed speed

  :param number p: print speed
  :param number f: feed speed

  Printer performance may vary based on the power supply voltage,
  thickness of paper, phase of the moon and other seemingly random
  variables.  This method sets the times (in microseconds) for the
  paper to advance one vertical 'dot' when printing and when feeding.
  For example, in the default initialized state, normal-sized text is
  24 dots tall and the line spacing is 30 dots, so the time for one
  line to be issued is approximately 24 * print time + 6 * feed time.
  The default print and feed times are based on a random test unit,
  but as stated above your reality may be influenced by many factors.
  This lets you tweak the timing to avoid excessive delays and/or
  overrunning the printer buffer.
  """
  def set_timers(self, p, f):
    self._dot_print_time = p
    self._dot_feed_time = f

  # Sets the default settings
  def set_default(self):
    self.online()
    self.justify('L')
    self.inverse_off()
    self.double_height_off()
    self.set_line_height(30)
    self.bold_off()
    self.underline_off()
    self.set_barcode_height(50)
    self.set_size('s')
    self.set_charset()
    self.set_code_page()

  # Put the printer into a low-energy state after the given number
  # of seconds.
  def sleep(self, seconds = 1):
    if self._firmware >= 264:
      self.write_bytes(ASCII_ESC, '8', seconds, seconds >> 8)
    else:
      self.write_bytes(ASCII_ESC, '8', seconds)

  def reset(self):
    self.write_bytes(ASCII_ESC, '@')
    self._column = 0
    self._max_column = 32
    self._char_height = 24
    self._line_spacing = 6
    self._barcode_height = 50
    self._cur_code_page = 0
    self.set_heat_config()
    if self._firmware >= 264:
      # Configure tab stops on recent printers
      self.write_bytes(ASCII_ESC, 'D') # Set tab stops...
      self.write_bytes(4, 8, 12, 16)   # ...every 4 columns,
      self.write_bytes(20, 24, 28, 0)  # 0 marks end-of-list.

  def wake(self):
    self.write_bytes(255) # Wake
    if self._firmware >= 264:
      sleep_ms(50)
      self.write_bytes(ASCII_ESC, '8', 0, 0) # Sleep off (important!)
    else:
      # Datasheet recommends a 50 ms delay before issuing further commands,
      # but in practice this alone isn't sufficient (e.g. text size/style
      # commands may still be misinterpreted on wake). A slightly longer
      # delay, interspersed with NUL chars (no-ops) seems to help.
      for i in range(10):
        self.write_bytes(0)
        sleep_ms(10)

  """
  Take the printer back online. Subsequent print commands will be obeyed.
  """
  def online(self):
    self.write_bytes(ASCII_ESC, '=', 1)

  """
  Take the printer offline. Print commands sent after this will be
  ignored until 'online' is called.
  """
  def offline(self):
    self.write_bytes(ASCII_ESC, '=', 0)

  def println(self, msg):
    self.print(msg)
    self.ln()

  def dln(self):
    self.ln()
    self.ln()

  def ln(self):
    self.print('\n')

  def print(self, msg):
    buffer = bytearray()
    for symbol in msg:
      # Mod symbol if it is in map
      if symbol in symbols_map:
        symbol = symbols_map[symbol]
      num = ord(symbol)
      # Process cyrilic symbols
      if num > 0x3D0:
        self.set_code_page(CODEPAGE_WCP1251)
        num -= 848
      buffer.append(num)
      # Calculate delay to feed a paper
      if symbol is '\n' or len(buffer) >= self._max_column:
        self._uart.write(buffer)
        buffer = bytearray()
        if self._prev_byte == '\n':
          sleep_us((self._char_height + self._line_spacing) * self._dot_feed_time)
        else:
          sleep_us((self._char_height * self._dot_print_time) + (self._line_spacing * self._dot_feed_time))
      self._prev_byte = symbol
    if len(buffer): self._uart.write(buffer)

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
    if self._firmware >= 268:
      self.write_bytes(ASCII_GS, 'B', 1)
    else:
      self.set_print_mode(INVERSE_MASK)

  def inverse_off(self):
    if self._firmware >= 268:
      self.write_bytes(ASCII_GS, 'B', 0)
    else:
      self.unset_print_mode(INVERSE_MASK)

  def upside_down_on(self):
    if self._firmware >= 268:
      self.write_bytes(ASCII_ESC, '{', 1)
    else:
      self.set_print_mode(UPDOWN_MASK)

  def upside_down_off(self):
    if self._firmware >= 268:
      self.write_bytes(ASCII_ESC, '{', 0)
    else:
      self.set_print_mode(UPDOWN_MASK)

  def set_print_mode(self, mask):
    self._print_mode |= mask
    self.write_print_mode()
    self._adjust_char_values(mask)

  def unset_print_mode(self, mask):
    self._print_mode &= (~mask) & 0xFF
    self.write_print_mode()
    self._adjust_char_values(mask)

  def _adjust_char_values(self, print_mode):
    char_width =0
    if print_mode & FONT_MASK:
      # FontB
      self._char_height = 17
      char_width = 9
    else:
      # FontA
      self._char_height = 24
      char_width = 12
    # Double Width Mode
    if print_mode & DOUBLE_WIDTH_MASK:
      self._max_column /= 2
      char_width *= 2
    # Double Height Mode
    if print_mode & DOUBLE_HEIGHT_MASK:
      self._char_height *= 2
    self._max_column = (384 / char_width)

  def set_line_height(self, val = 30):
    if val < 24:
      val = 24
    self._line_spacing = 24
    # The printer doesn't take into account the current text height
    # when setting line height, making this more akin to inter-line
    # spacing. Default line spacing is 30 (char height of 24, line
    # spacing of 6).
    self.write_bytes(ASCII_ESC, '3', val)

  def feed(self, lines):
    """
    Feeds by the specified number of lines
    """
    if self._firmware >= 264:
      self.write_bytes(ASCII_ESC, 'd', lines)
      sleep_us(self._dot_feed_time * self._char_height)
    else:
      for i in range(lines):
        self.ln()

  def feed_rows(self, rows):
    """
    Feeds by the specified number of individual pixel rows
    """
    self.write_bytes(ASCII_ESC, 'J', rows)
    sleep_us(rows * self._dot_feed_time)

  """
  Flush data pending in the printer 
  """
  def flush(self):
    self.write_bytes(ASCII_FF)

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
    self._barcode_height = val
    self.write_bytes(ASCII_GS, 'h', val)

  def print_barcode(self, text, barcode_type):
    self.feed(1)
    if self._firmware >= 264:
      barcode_type += 65
    self.write_bytes(ASCII_GS, 'H', 2) # Print label below barcode
    self.write_bytes(ASCII_GS, 'w', 3) # Barcode width 3 (0.375/1.0mm thin/thick)
    self.write_bytes(ASCII_GS, 'k', 3) # Barcode type (listed in .h file)
    if self._firmware >= 264:
      size = len(text)
      if (size > 255):
        size = 255
      self.write_bytes(size)
      for i in range(0, size - 1):
        self.write_bytes(text[i])
    else:
      for i in range(0, len(text) - 1):
        self.write_bytes(text[i])
    sleep_us((self._barcode_height + 40) * self._dot_print_time)

  """
  Alters some chars in ASCII 0x23-0x7E range; see datasheet
  
  :param num val: Value of the desired character set
  """
  def set_charset(self, val = 0):
    if val > 15:
      val = 15
    self.write_bytes(ASCII_ESC, 'R', val)

  def set_code_page(self, val = 0):
    """
    Selects alt symbols for 'upper' ASCII values 0x80-0xFF

    :param num val: Value of the desired character code page
    """
    if val > 47:
      val = 47
    if self._cur_code_page is val: return
    self._cur_code_page = val
    self.write_bytes(ASCII_ESC, 't', val)

  """
  Sets print head heating configuration
  
  dots max printing dots, 8 dots per increment
  time heating time, 10us per increment
  interval heating interval, 10 us per increment

  ESC 7 n1 n2 n3 Setting Control Parameter Command
  n1 = "max heating dots" 0-255 -- max number of thermal print head
      elements that will fire simultaneously.  Units = 8 dots (minus 1).
      Printer default is 7 (64 dots, or 1/6 of 384-dot width), this code
      sets it to 11 (96 dots, or 1/4 of width).
  n2 = "heating time" 3-255 -- duration that heating dots are fired.
      Units = 10 us.  Printer default is 80 (800 us), this code sets it
      to value passed (default 120, or 1.2 ms -- a little longer than
      the default because we've increased the max heating dots).
  n3 = "heating interval" 0-255 -- recovery time between groups of
      heating dots on line; possibly a function of power supply.
      Units = 10 us.  Printer default is 2 (20 us), this code sets it
      to 40 (throttled back due to 2A supply).
  More heating dots = more peak current, but faster printing speed.
  More heating time = darker print, but slower printing speed and
  possibly paper 'stiction'.  More heating interval = clearer print,
  but slower printing speed.
  """
  def set_heat_config(self, dots = 11, time = 120, interval = 40):
    self.write_bytes(ASCII_ESC, '7') # Esc 7 (print settings)
    self.write_bytes(dots, time, interval) # Heating dots, heat time, heat interval

  """
  Prints a bitmap

  w Width of the image in pixels
  h Height of the image in pixels
  bitmap Bitmap data, from a file.
  fromProgMem
  """
  # def print_bitmap(self, w, h, bitmap):
  #   row_bytes = (w + 7) / 8 # Round up to next byte boundary
  #   row_bytes_clipped = 48 if row_bytes >= 48 else row_bytes

  #   chunk_height_limit = 256 / row_bytes_clipped
  #   if chunk_height_limit > self._max_chunk_height:
  #     chunk_height_limit = self._max_chunk_height
  #   elif chunk_height_limit < 1:
  #     chunk_height_limit = 1

  #   row_start = 0
  #   for i in range(0, h - 1, row_start):


  def write_bytes(self, *items):
    arr = []
    for item in items:
      if type(item) is str:
        arr.append(ord(item[0]))
      else:
        arr.append(item)
    self._uart.write(bytes(arr))
