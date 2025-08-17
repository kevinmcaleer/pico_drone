# Flight Computer Integration Test (Skeleton)
import unittest
from imu_gy91 import IMUGY91
from mag_gy273 import MagnetometerGY273
from gps_neo6m import GPSNEO6M

class DummyI2C:
    def writeto_mem(self, *args, **kwargs):
        pass
    def readfrom_mem(self, addr, reg, n):
        return bytes([0, 0] * (n // 2))
class DummyUART:
    def any(self):
        return False
    def read(self, n):
        return b''

class TestFlightComputer(unittest.TestCase):
    def setUp(self):
        self.imu = IMUGY91(DummyI2C())
        self.mag = MagnetometerGY273(DummyI2C())
        self.gps = GPSNEO6M(DummyUART())
    def test_integration(self):
        imu_data = self.imu.read_all(0.01)
        heading = self.mag.calculate_heading(1, 1)
        self.assertIsInstance(imu_data, dict)
        self.assertIsInstance(heading, float)

if __name__ == "__main__":
    unittest.main()
