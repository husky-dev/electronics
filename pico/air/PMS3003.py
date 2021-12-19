

"""
# PM2.5 laser dust sensor

Wiki: https://wiki.dfrobot.com/PM2.5_laser_dust_sensor_SKU_SEN0177

Example of the package:
b'BM\x00\x14\x00\x0c\x00\x11\x00\x11\x00\x0c\x00\x11\x00\x11\x02\x8e\x00\x05\x97\x00\x02+'

- BM - 0x42 and 0x4d - start bits
- x00\x14 - the size of the package (20 in this case)

- x00\x0c - PM1.0
- x00\x11 - PM2.5
- x00\x11 - PM10

- x00\x02+ - checksum of the all bits
"""

def validate_package(msg):
  if len(msg) is not 24: raise Exception("Data package is not 24 bits long")
  if msg[0] is not 0x42: raise Exception("First bit should be 0x42")
  if msg[1] is not 0x4d: raise Exception("Second bit should be 0x4d")

  msg_sum = 0
  for i in range(0, len(msg) - 2):
    msg_sum += msg[i]
  check_sum = (msg[len(msg) - 2] << 8) + msg[len(msg) - 1]
  if check_sum is not msg_sum: raise Exception("Wrong checksum")
  

def package_to_data(msg):
  pm01 = (msg[4] << 8) + msg[5]
  # print('PM1.0= %d ug/m3' % pm01)
  pm2_5 = (msg[6] << 8) + msg[7]
  # print('PM2.5= %d ug/m3' % pm2_5)
  pm10 = (msg[8] << 8) + msg[9]
  # print('PM10= %d ug/m3' % pm10)
  return { 'pm01': pm01, 'pm2.5': pm2_5, 'pm10': pm10 }

class PMS3003:
  def __init__(self, uart):
    self._uart = uart

  def read_data(self):
    while True:
      msg = self._uart.read(24)
      if not msg: continue
      if msg[0] is not 0x42: continue
      validate_package(msg)
      return package_to_data(msg)
