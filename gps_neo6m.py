# gps_neo6m.py
"""
Module for interfacing with a NEO-6M compatible GPS module on the Raspberry Pi Pico 2W using MicroPython.
"""
import time

class GPSNEO6M:
    def __init__(self, uart):
        self.uart = uart
        self.buffer = b''

    def read_sentence(self):
        while self.uart.any():
            self.buffer += self.uart.read(1)
            if b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                return line.decode('utf-8').strip()
        return None

    def parse_gpgga(self, sentence):
        # Example: $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
        parts = sentence.split(',')
        if parts[0] != '$GPGGA':
            return None
        try:
            lat = self._parse_lat(parts[2], parts[3])
            lon = self._parse_lon(parts[4], parts[5])
            alt = float(parts[9])
            return {'lat': lat, 'lon': lon, 'alt': alt}
        except Exception:
            return None

    def _parse_lat(self, raw, hemi):
        if not raw:
            return None
        deg = float(raw[:2])
        min = float(raw[2:])
        val = deg + min / 60.0
        if hemi == 'S':
            val = -val
        return val

    def _parse_lon(self, raw, hemi):
        if not raw:
            return None
        deg = float(raw[:3])
        min = float(raw[3:])
        val = deg + min / 60.0
        if hemi == 'W':
            val = -val
        return val

    def get_location(self):
        while True:
            sentence = self.read_sentence()
            if sentence and sentence.startswith('$GPGGA'):
                data = self.parse_gpgga(sentence)
                if data:
                    return data
            time.sleep(0.1)
