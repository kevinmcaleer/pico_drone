# drv8833.py
"""
DRV8833 Motor Driver class for MicroPython (Raspberry Pi Pico)
Supports forward, reverse, brake, and coast for a single motor.
"""
try:
    from machine import Pin, PWM
except ImportError:
    # For local testing
    class Pin:
        OUT = 0
        def __init__(self, pin, mode):
            self.state = 0
        def high(self):
            self.state = 1
        def low(self):
            self.state = 0
    class PWM:
        def __init__(self, pin):
            self.duty_u16 = lambda x: None

class DRV8833:
    def __init__(self, in1, in2, pwm=False):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.pwm = pwm
        if pwm:
            self.pwm1 = PWM(self.in1)
            self.pwm2 = PWM(self.in2)
    def forward(self, speed=65535):
        if self.pwm:
            self.pwm1.duty_u16(speed)
            self.pwm2.duty_u16(0)
        else:
            self.in1.high()
            self.in2.low()
    def reverse(self, speed=65535):
        if self.pwm:
            self.pwm1.duty_u16(0)
            self.pwm2.duty_u16(speed)
        else:
            self.in1.low()
            self.in2.high()
    def brake(self):
        if self.pwm:
            self.pwm1.duty_u16(65535)
            self.pwm2.duty_u16(65535)
        else:
            self.in1.high()
            self.in2.high()
    def coast(self):
        if self.pwm:
            self.pwm1.duty_u16(0)
            self.pwm2.duty_u16(0)
        else:
            self.in1.low()
            self.in2.low()
