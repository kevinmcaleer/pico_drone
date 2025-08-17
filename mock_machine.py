# mock_machine.py
"""
Mock machine module for testing MicroPython code on standard Python.
Provides dummy I2C, Pin, and UART classes.
"""
class I2C:
    def __init__(self, *args, **kwargs):
        pass
    def writeto_mem(self, *args, **kwargs):
        pass
    def readfrom_mem(self, *args, **kwargs):
        return bytes([0, 0])

class Pin:
    def __init__(self, *args, **kwargs):
        pass

class UART:
    def __init__(self, *args, **kwargs):
        pass
    def any(self):
        return False
    def read(self, n):
        return b''
