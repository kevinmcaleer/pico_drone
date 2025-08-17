# Test for Magnetometer GY-273 module
import unittest
from mag_gy273 import MagnetometerGY273

class DummyI2C:
    def writeto_mem(self, *args, **kwargs):
        pass
    def readfrom_mem(self, addr, reg, n):
        return bytes([0, 0, 0, 0, 0, 0])

class TestMagnetometerGY273(unittest.TestCase):
    def setUp(self):
        self.mag = MagnetometerGY273(DummyI2C())
    def test_read_raw(self):
        x, y, z = self.mag.read_raw()
        self.assertIsInstance(x, int)
    def test_heading(self):
        heading = self.mag.calculate_heading(1, 1)
        self.assertIsInstance(heading, float)

if __name__ == "__main__":
    unittest.main()
