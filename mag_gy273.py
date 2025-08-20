
# mag_gy273.py (QMC5883L version for GY-273 clones)
"""
Module for interfacing with the GY-273 (QMC5883L) magnetometer sensor on the Raspberry Pi Pico 2W using MicroPython.
"""
try:
    from machine import I2C
except ImportError:
    from mock_machine import I2C

MAG_ADDR = 0x0D  # QMC5883L default address

class MagnetometerGY273:
    def __init__(self, i2c):
        self.i2c = i2c
        self._init_sensor()

    def _init_sensor(self):
        # QMC5883L: Set to continuous mode, 200Hz, 8G range, OSR=512
        # Control register 1: 0x09
        # 0b00011101 = 0x1D: OSR=512, RNG=8G, ODR=200Hz, MODE=Continuous
        self.i2c.writeto_mem(MAG_ADDR, 0x09, bytearray([0x1D]))  # Use bytearray for MicroPython compatibility

    def read_raw(self):
        data = self.i2c.readfrom_mem(MAG_ADDR, 0x00, 6)  # All positional args
        x = int.from_bytes(data[0:2], 'little')
        if x >= 32768:
            x -= 65536
        y = int.from_bytes(data[2:4], 'little')
        if y >= 32768:
            y -= 65536
        z = int.from_bytes(data[4:6], 'little')
        if z >= 32768:
            z -= 65536
        return x, y, z

    def calculate_heading(self, x, y):
        import math
        heading = math.atan2(y, x)
        heading = math.degrees(heading)
        if heading < 0:
            heading += 360
        return heading

    def read_heading(self):
        x, y, z = self.read_raw()
        return self.calculate_heading(x, y)
