# mag_gy273.py
"""
Module for interfacing with the GY-273 magnetometer sensor on the Raspberry Pi Pico 2W using MicroPython.
"""
try:
    from machine import I2C
except ImportError:
    from mock_machine import I2C

MAG_ADDR = 0x1E  # Example address for HMC5883L (GY-273)

class MagnetometerGY273:
    def __init__(self, i2c):
        self.i2c = i2c
        self._init_sensor()

    def _init_sensor(self):
        # Example: set to continuous measurement mode
        self.i2c.writeto_mem(MAG_ADDR, 0x02, b'\x00')

    def read_raw(self):
        data = self.i2c.readfrom_mem(MAG_ADDR, 0x03, 6)
        x = int.from_bytes(data[0:2], 'big', signed=True)
        z = int.from_bytes(data[2:4], 'big', signed=True)
        y = int.from_bytes(data[4:6], 'big', signed=True)
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
