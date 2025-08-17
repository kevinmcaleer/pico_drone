# Test for GPS NEO-6M module
import unittest
from gps_neo6m import GPSNEO6M


# Dummy UART for normal operation
class DummyUART:
    def __init__(self):
        self.data = b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\n"
    def any(self):
        return len(self.data) > 0
    def read(self, n):
        d, self.data = self.data[:n], self.data[n:]
        return d

# Dummy UART for malformed sentence
class MalformedUART:
    def __init__(self):
        self.data = b"$GPGGA,not,a,valid,sentence\n"
    def any(self):
        return len(self.data) > 0
    def read(self, n):
        d, self.data = self.data[:n], self.data[n:]
        return d

# Dummy UART for raising exception
class FailingUART:
    def any(self):
        raise RuntimeError("UART failure")
    def read(self, n):
        raise RuntimeError("UART failure")


class TestGPSNEO6M(unittest.TestCase):
    def setUp(self):
        self.gps = GPSNEO6M(DummyUART())

    def test_parse_gpgga(self):
        sentence = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
        data = self.gps.parse_gpgga(sentence)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        if data is not None:
            self.assertIn('lat', data)
            self.assertIn('lon', data)
            self.assertIn('alt', data)

    def test_get_location_success(self):
        gps = GPSNEO6M(DummyUART())
        result = gps.get_location(max_attempts=5)
        self.assertIsNotNone(result)
        if result is not None:
            self.assertIn('lat', result)

    def test_get_location_malformed(self):
        gps = GPSNEO6M(MalformedUART())
        result = gps.get_location(max_attempts=3)
        self.assertIsNone(result)

    def test_get_location_uart_failure(self):
        logs = []
        def logger(msg):
            logs.append(msg)
        gps = GPSNEO6M(FailingUART())
        result = gps.get_location(max_attempts=2, logger=logger)
        self.assertIsNone(result)
        self.assertTrue(any("GPS read error" in log for log in logs))
        self.assertTrue(any("No valid location" in log for log in logs))

if __name__ == "__main__":
    unittest.main()
