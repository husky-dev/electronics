from machine import UART
from time import sleep
from thermal_printer import Thermal_Printer, CODEPAGE_WCP1251

printer = Thermal_Printer(UART(1, baudrate=19200))

def demo():
  printer.reset()
  printer.println('Ґанок в Україні')
  printer.feed(2)

def demo001():
  # Font options
  printer.set_font('B')
  printer.println('FontB')
  printer.println('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  printer.set_font('A')
  printer.println('FontA (default)')
  printer.println('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

  # Test inverse on & off
  printer.inverse_on()
  printer.println('Inverse ON')
  printer.inverse_off()

  # Test character double-height on & off
  printer.double_height_on()
  printer.println('Double Height ON')
  printer.double_height_off()

  # Set text justification (right, center, left) -- accepts 'L', 'C', 'R'
  printer.justify('R')
  printer.println('Right justified')
  printer.justify('C')
  printer.println('Center justified')
  printer.justify('L')
  printer.println('Left justified')

  # Test more styles
  printer.bold_on()
  printer.println('Bold text')
  printer.bold_off()

  printer.underline_on()
  printer.println('Underlined text')
  printer.underline_off()

  printer.set_size('L')        # Set type size, accepts 'S', 'M', 'L'
  printer.println('Large')
  printer.set_size('M')
  printer.println('Medium')
  printer.set_size('S')
  printer.println('Small')

  # printer.justify('C')
  # printer.println('normal\nline\nspacing')
  # printer.set_line_height(50)
  # printer.println('Taller\nline\nspacing')
  # printer.set_line_height() # Reset to default
  # printer.justify('L')

  # Barcode examples:
  # CODE39 is the most common alphanumeric barcode:
  # printer.printBarcode('ADAFRUT', CODE39)
  # printer.setBarcodeHeight(100)
  # Print UPC line on product barcodes:
  # printer.printBarcode('123456789123', UPC_A)

  # Print the 75x75 pixel logo in adalogo.h:
  # printer.printBitmap(adalogo_width, adalogo_height, adalogo_data)

  # Print the 135x135 pixel QR code in adaqrcode.h:
  # printer.printBitmap(adaqrcode_width, adaqrcode_height, adaqrcode_data)
  # printer.println('Adafruit!')
  # printer.feed(2)

  # printer.sleep()      # Tell printer to sleep
  # delay(3000L)         # Sleep for 3 seconds
  # printer.wake()       # MUST wake() before printing again, even if reset
  # printer.setDefault() # Restore printer to defaults
  