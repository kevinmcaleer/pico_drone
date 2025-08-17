# Test for GPS NEO-6M module
import unittest
from gps_neo6m import GPSNEO6M

class DummyUART:
    def __init__(self):
        self.data = b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\n"
    def any(self):
        return len(self.data) > 0
    def read(self, n):
        d, self.data = self.data[:n], self.data[n:]
        return d

class TestGPSNEO6M(unittest.TestCase):
    def setUp(self):
        self.gps = GPSNEO6M(DummyUART())
    def test_parse_gpgga(self):
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
        data = self.gps.parse_gpgga(sentence)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertIn('lat', data)
        self.assertIn('lon', data)
        self.assertIn('alt', data)

if __name__ == "__main__":
    unittest.main()
