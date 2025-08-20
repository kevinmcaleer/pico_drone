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
    """Simple DRV8833 half-bridge wrapper for a single brushed DC motor.

    When pwm=True we attach independent PWM channels to each input pin.
    Forward drives IN1 with PWM and holds IN2 low. Reverse is the opposite.

    brake(): both inputs HIGH (active brake)
    coast(): both inputs LOW (freewheel)
    set_speed(duty): convenience forward speed (0-65535)
    """

    def __init__(self, in1, in2, pwm=False, freq=20000):
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.pwm = pwm
        if pwm:
            # Create PWM objects; rely on default frequency.
            self.pwm1 = PWM(self.in1)
            self.pwm2 = PWM(self.in2)
        # default state coast
        self.coast()

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

    def set_speed(self, duty):
        if not self.pwm:
            raise RuntimeError("PWM not enabled for this motor")
        if duty < 0:
            # simple bidirectional: negative -> reverse
            d = min(65535, -duty)
            self.reverse(d)
        else:
            d = min(65535, duty)
            self.forward(d)

    def brake(self):
        if self.pwm:
            # Active brake: both high (could also set both low then high briefly)
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


class _Channel:
    """Internal helper representing one motor channel of a DRV8833 chip."""
    def __init__(self, in1, in2, pwm=False):
        self.pwm = pwm
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        if pwm:
            self.p1 = PWM(self.in1)
            self.p2 = PWM(self.in2)
            # default coast
            self.p1.duty_u16(0)
            self.p2.duty_u16(0)
        else:
            self.in1.low()
            self.in2.low()
    def forward(self, duty=65535):
        if self.pwm:
            self.p1.duty_u16(duty)
            self.p2.duty_u16(0)
        else:
            self.in1.high()
            self.in2.low()
    def reverse(self, duty=65535):
        if self.pwm:
            self.p1.duty_u16(0)
            self.p2.duty_u16(duty)
        else:
            self.in1.low()
            self.in2.high()
    def brake(self):
        if self.pwm:
            self.p1.duty_u16(65535)
            self.p2.duty_u16(65535)
        else:
            self.in1.high()
            self.in2.high()
    def coast(self):
        if self.pwm:
            self.p1.duty_u16(0)
            self.p2.duty_u16(0)
        else:
            self.in1.low()
            self.in2.low()


class DRV8833Chip:
    """Represents a full DRV8833 device (two H-bridges / two brushed motors).

    Usage:
        chip = DRV8833Chip(ain1, ain2, bin1, bin2, pwm=True)
        chip.motor_a.forward(30000)
        chip.motor_b.reverse(20000)

    Each motor channel has: forward(duty), reverse(duty), brake(), coast().
    """
    def __init__(self, ain1, ain2, bin1, bin2, pwm=False):
        self.motor_a = _Channel(ain1, ain2, pwm=pwm)
        self.motor_b = _Channel(bin1, bin2, pwm=pwm)
        self.pwm = pwm

    def set(self, motor, duty):
        ch = self.motor_a if motor in ('a','A',0,'motor_a') else self.motor_b
        if duty < 0:
            ch.reverse(min(65535, -duty))
        else:
            ch.forward(min(65535, duty))
