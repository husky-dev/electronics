from machine import UART
from time import sleep
from thermal_printer import Thermal_Printer

printer = Thermal_Printer(UART(1, baudrate=19200))

def p():
  printer.double_height_on()
  sleep(1)
  printer.println('Задачи на сегодня:')
  sleep(1)
  printer.double_height_off()
  sleep(1)
  printer.feed(1)
  sleep(1)
  printer.println('- Одно')
  sleep(1)
  printer.println('- Второе')
  sleep(1)
  printer.println('- Третье')
  sleep(1)
  printer.println('- Пьятое')
  sleep(1)
  printer.println('- Десятое')
  sleep(1)
  printer.feed(2)