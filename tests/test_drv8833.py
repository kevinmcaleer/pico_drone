# test_drv8833.py
import unittest
from drv8833 import DRV8833

class DummyPin:
    OUT = 0
    def __init__(self, pin, mode):
        self.state = None
    def high(self):
        self.state = 1
    def low(self):
        self.state = 0

class DummyPWM:
    def __init__(self, pin):
        self.duty = 0
    def duty_u16(self, val):
        self.duty = val

class TestDRV8833(unittest.TestCase):
    def setUp(self):
        # Patch Pin and PWM for local test
        import drv8833
        drv8833.Pin = DummyPin
        drv8833.PWM = DummyPWM
        self.motor = DRV8833(2, 3, pwm=False)
        self.motor_pwm = DRV8833(2, 3, pwm=True)
    def test_forward(self):
        self.motor.forward()
        self.assertEqual(self.motor.in1.state, 1)
        self.assertEqual(self.motor.in2.state, 0)
    def test_reverse(self):
        self.motor.reverse()
        self.assertEqual(self.motor.in1.state, 0)
        self.assertEqual(self.motor.in2.state, 1)
    def test_brake(self):
        self.motor.brake()
        self.assertEqual(self.motor.in1.state, 1)
        self.assertEqual(self.motor.in2.state, 1)
    def test_coast(self):
        self.motor.coast()
        self.assertEqual(self.motor.in1.state, 0)
        self.assertEqual(self.motor.in2.state, 0)
    def test_pwm_forward(self):
        self.motor_pwm.forward(12345)
        self.assertEqual(self.motor_pwm.pwm1.duty, 12345)
        self.assertEqual(self.motor_pwm.pwm2.duty, 0)
    def test_pwm_reverse(self):
        self.motor_pwm.reverse(54321)
        self.assertEqual(self.motor_pwm.pwm1.duty, 0)
        self.assertEqual(self.motor_pwm.pwm2.duty, 54321)
    def test_pwm_brake(self):
        self.motor_pwm.brake()
        self.assertEqual(self.motor_pwm.pwm1.duty, 65535)
        self.assertEqual(self.motor_pwm.pwm2.duty, 65535)
    def test_pwm_coast(self):
        self.motor_pwm.coast()
        self.assertEqual(self.motor_pwm.pwm1.duty, 0)
        self.assertEqual(self.motor_pwm.pwm2.duty, 0)

if __name__ == "__main__":
    unittest.main()
