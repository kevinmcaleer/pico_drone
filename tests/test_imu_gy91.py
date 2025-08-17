# Test for IMU GY-91 module
import unittest
from imu_gy91 import IMUGY91

class DummyI2C:
    def writeto_mem(self, *args, **kwargs):
        pass
    def readfrom_mem(self, addr, reg, n):
        # Return 3 bytes for BMP280 registers, else 2 bytes
        if n == 3:
            return bytes([0, 0, 0])
        return bytes([0, 0] * (n // 2))

class TestIMUGY91(unittest.TestCase):
    def setUp(self):
        self.imu = IMUGY91(DummyI2C())
    def test_read_accel(self):
        ax, ay, az = self.imu.read_accel()
        self.assertIsInstance(ax, float)
    def test_read_gyro(self):
        gx, gy, gz = self.imu.read_gyro()
        self.assertIsInstance(gx, float)
    def test_read_bmp280(self):
        temp, press = self.imu.read_bmp280()
        self.assertIsInstance(temp, float)
    def test_orientation(self):
        pitch, roll = self.imu.get_orientation(0.01)
        self.assertIsInstance(pitch, float)

if __name__ == "__main__":
    unittest.main()
