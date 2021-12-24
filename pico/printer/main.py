from machine import UART
from time import sleep
from thermal_printer import Thermal_Printer, CODE39, UPC_A, CODEPAGE_WCP1251

printer = Thermal_Printer(UART(1, baudrate=19200), firmware = 268)

def demo():
  # printer.inverse_on()
  # printer.println(' 20.12.2021 (Четверг) ')
  # printer.inverse_off()
  printer.set_size('M')
  printer.println('Погода:')
  printer.set_size('S')

def print_header(val):
  printer.bold_on()
  printer.println(val)
  printer.bold_off()

def print_spliter():
  printer.feed(1)

def main():
  # printer.wake()
  # printer.reset()
  # printer.flush()

  printer.inverse_on()
  # printer.println(' 20.12.2021 (Четверг) ')
  printer.println(' Hello world ')
  sleep(1)
  printer.inverse_off()

  # print_header('Погода:')
  # printer.println('+3 ... +9 (ясно)')
  # print_spliter()

  # print_header('Задачі:')
  # printer.println('- Один')
  # printer.println('- Два')
  # printer.println('- Три')
  # print_spliter()

  # print_header('Курс валют:')
  # printer.println('USD: 27.24')
  # printer.println('EUR: 30.82')
  # print_spliter()

  # print_header('Цитата:')
  # printer.println('Рискуй. Удача любит смелых')
  # printer.justify('R')
  # printer.bold_on()
  # printer.println('Річард Бренсон')
  # printer.bold_off()
  # printer.justify('L')
  # print_spliter()

  # printer.sleep()


def demo_001():
  printer.wake()
  printer.reset()
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

  printer.justify('C')
  printer.println('normal\nline\nspacing')
  printer.set_line_height(50)
  printer.println('Taller\nline\nspacing')
  printer.set_line_height() # Reset to default
  printer.justify('L')

  # Barcode examples:
  # CODE39 is the most common alphanumeric barcode:
  printer.print_barcode('ADAFRUT', CODE39)
  printer.set_barcode_height(100)
  # Print UPC line on product barcodes:
  printer.print_barcode('123456789123', UPC_A)

  # Print the 75x75 pixel logo in adalogo.h:
  # printer.printBitmap(adalogo_width, adalogo_height, adalogo_data)

  # Print the 135x135 pixel QR code in adaqrcode.h:
  # printer.printBitmap(adaqrcode_width, adaqrcode_height, adaqrcode_data)
  # printer.println('Adafruit!')
  # printer.feed(2)

  printer.sleep()      # Tell printer to sleep
  sleep(3)             # Sleep for 3 seconds
  printer.wake()       # MUST wake() before printing again, even if reset
  printer.set_default() # Restore printer to defaults
  