"""
Interface to a BME280 sensor with the i2c bus of the Pico

Based on https://github.com/codesqueak/pi_pico_bme280
"""
from time import sleep

reg_base_addr = 0x88

class BME280:
  def __init__(self, i2c, addr = 0x76):
    self._i2c = i2c
    self._i2c_addr = addr
    self._setup()

  def _setup(self):
    # All setup parameters are defined in the datasheet
    # https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf
    #
    # humidity  oversampling
    self._i2c.writeto_mem(self._i2c_addr, 0xf2, b'\x03')  # ctrl_hum 00000 011
    # temp oversampling / pressure / oversampling / sensor mode
    self._i2c.writeto_mem(self._i2c_addr, 0xf4, b'\x6F')  # ctrl_meas 011 011 11
    # wait for it to take effect
    sleep(0.1)

  def _read_sensor_memory(self):
    #
    # The sensor presents as a memory mapped device on teh i2c bus
    #
    block_size = 0x100 - reg_base_addr  # bytes to read
    self._r = self._i2c.readfrom_mem(self._i2c_addr, reg_base_addr, block_size)  # Read the sensor into a buffer

    # get compensation parameters (These are constants, only read once in a production system)
    self._dig_t1 = self._read_const_u(0x88)
    self._dig_t2 = self._read_const_s(0x8a)
    self._dig_t3 = self._read_const_s(0x8c)

    # get compensation parameters (These are constants, only read once in a production system)
    self._dig_p1 = self._read_const_u(0x8e)
    self._dig_p2 = self._read_const_s(0x90)
    self._dig_p3 = self._read_const_s(0x92)
    self._dig_p4 = self._read_const_s(0x94)
    self._dig_p5 = self._read_const_s(0x96)
    self._dig_p6 = self._read_const_s(0x98)
    self._dig_p7 = self._read_const_s(0x9a)
    self._dig_p8 = self._read_const_s(0x9c)
    self._dig_p9 = self._read_const_s(0x9e)

    # get compensation parameters (These are constants, only read once in a production system)
    self._dig_h1 = self._r[0xa1 - reg_base_addr]
    self._dig_h2 = self._read_const_s(0xe1)
    self._dig_h3 = self._r[0xe3 - reg_base_addr]
    self._dig_h4 = (self._r[0xe4 - reg_base_addr] << 4) + (self._r[0xe5 - reg_base_addr] & 0x0f)
    self._dig_h5 = (self._r[0xe6 - reg_base_addr] << 4) + ((self._r[0xe5 - reg_base_addr] & 0x00f0) >> 4)
    self._dig_h6 = self._r[0xe7 - reg_base_addr]


  # read two bytes as an unsigned int
  def _read_const_u(self, a):
      return self._r[a - reg_base_addr] + (self._r[a - reg_base_addr + 1] << 8)


  # read two bytes as a signed int
  def _read_const_s(self, a):
      v = self._r[a - reg_base_addr] + (self._r[a - reg_base_addr + 1] << 8)
      if v > 32767:
          v = v - 65536
      return v

  def read_data(self):
    self._read_sensor_memory()

    # TEMPERATURE

    # get raw temperature
    temp_msb = self._r[0xfa - reg_base_addr]
    temp_lsb = self._r[0xfb - reg_base_addr]
    temp_xlsb = self._r[0xfc - reg_base_addr]
    adc_t = (temp_msb << 12) + (temp_lsb << 4) + (temp_xlsb >> 4)
    # calc temperature
    # Shown as done in the datasheet - can be tidied up
    var1 = ((adc_t >> 3) - (self._dig_t1 << 1)) * (self._dig_t2 >> 11)
    var2 = (((((adc_t >> 4) - self._dig_t1) * ((adc_t >> 4) - self._dig_t1)) >> 12) * self._dig_t3) >> 14
    t_fine = (var1 + var2)
    t = (t_fine * 5 + 128) >> 8
    tempr = t / 100

    press_msb = self._r[0xf7 - reg_base_addr]
    press_lsb = self._r[0xf8 - reg_base_addr]
    press_xlsb = self._r[0xf9 - reg_base_addr]
    adc_p = (press_msb << 12) + (press_lsb << 4) + (press_xlsb >> 4)
    # calc pressure
    # Shown as done in the datasheet - can be tidied up
    var1 = t_fine - 128000
    var2 = var1 * var1 * self._dig_p6
    var2 = var2 + ((var1 * self._dig_p5) << 17)
    var2 = var2 + (self._dig_p4 << 35)
    var1 = ((var1 * var1 * self._dig_p3) >> 8) + ((var1 * self._dig_p2) << 12)
    var1 = ((1 << 47) + var1) * self._dig_p1 >> 33
    if var1 == 0:  # divide by zero check
      p = 0
    else:
      p = 1048576 - adc_p
      p = int((((p << 31) - var2) * 3125) / var1)
      var1 = (self._dig_p9 * (p >> 13) * (p >> 13)) >> 25
      var2 = (self._dig_p8 * p) >> 19
      p = ((p + var1 + var2) >> 8) + (self._dig_p7 << 4)

    preasure = p / 25600

    # HUMIDITY

    # get raw pressure
    hum_msb = self._r[0xfd - reg_base_addr]
    hum_lsb = self._r[0xfe - reg_base_addr]
    adc_h = (hum_msb << 8) + hum_lsb

    # calc humidity
    # Shown as done in the datasheet - can be tidied up
    v_x1_u32r = t_fine - 76800

    v_x1_u32r = (((((adc_h << 14) - (self._dig_h4 << 20) - (self._dig_h5 * v_x1_u32r)) + 16384) >> 15) * (((((((v_x1_u32r * (
        self._dig_h6)) >> 10) * (((v_x1_u32r * self._dig_h3) >> 11) + 32768)) >> 10) + 2097152) * self._dig_h2 + 8192) >> 14))

    v_x1_u32r = (v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * self._dig_h1) >> 4))

    # limit checks
    if v_x1_u32r < 0:
        v_x1_u32r = 0

    if v_x1_u32r > 0x19000000:
        v_x1_u32r = 0x19000000

    h = v_x1_u32r >> 12

    humidity = h / 1024


    return { 'temperature': tempr, 'preasure': preasure, 'humidity': humidity }
