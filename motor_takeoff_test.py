"""
motor_takeoff_test.py

Simple motor test script to (a) verify each motor spins, then (b) perform a
brief "takeoff" style throttle ramp: slow ramp up -> hold ~2s -> ramp down.

SAFETY FIRST:
 - REMOVE PROPS for initial testing. Only attach propellers after you are 100% sure
   motor directions and throttle logic are correct.
 - Secure the frame so it cannot jump unexpectedly.
 - Have a way to cut power quickly (unplug battery / USB) if anything behaves oddly.

Assumptions:
 - Using DRV8833 half-bridges, one motor per DRV8833 channel (two pins per motor).
 - Pins below are placeholders; adjust to match your wiring.
 - If you only have one motor connected, leave the rest commented out.

Directions:
 1. Edit MOTOR_PINS to match each motor's (IN1, IN2) pin numbers.
 2. (Optional) Set USE_PWM = True if you wired the pins to PWM-capable GPIO and
    want variable speed; otherwise it will just switch full on/off.
 3. Copy to Pico, run: import motor_takeoff_test
 4. Observe console output. Ctrl+C aborts and brakes all motors.

RAMP PROFILE:
 - Countdown 3..1 (motors off)
 - Spin-up check (low duty)
 - Ramp to target over RAMP_UP_TIME seconds
 - Hold TARGET_SPEED for HOLD_TIME seconds ("takeoff" window)
 - Ramp down over RAMP_DOWN_TIME seconds
 - Brake & coast

You can tune constants at the top for different behaviors.
"""

try:
    from machine import Pin
except ImportError:  # Fallback for local testing
    class Pin:
        OUT = 0
        def __init__(self, n, mode):
            self.n = n
            self.state = 0
        def high(self):
            self.state = 1
        def low(self):
            self.state = 0

from time import sleep
from drv8833 import DRV8833

# ---------------- Configuration -----------------

# Motor mapping: logical name -> (IN_A, IN_B)
# Update these to match the diagram labels (example pins shown). Replace with actual from schematic:
MOTOR_PINS = {
    "top_left": (2, 3),
    "bottom_left": (4, 5),
    "top_right": (6, 7),
    "bottom_right": (8, 9),
}

USE_PWM = True           # All motors use PWM per user request
SPIN_CHECK_SPEED = 14000 # Very low duty to verify spin (if PWM). Ignored if not PWM.
TARGET_SPEED = 40000     # Hover-ish test duty (adjust!). Ignored if not PWM.
RAMP_UP_TIME = 1.0       # Seconds to ramp from spin check to target
HOLD_TIME = 2.0          # Seconds to hold at target ("takeoff" window)
RAMP_DOWN_TIME = 1.0     # Seconds to ramp down to 0
RAMP_STEPS = 20          # Granularity of ramp

# ------------------------------------------------

class MotorGroup:
    def __init__(self, motor_pins_map, use_pwm=False):
        self.motors = {}
        for name, pins in motor_pins_map.items():
            in1, in2 = pins
            self.motors[name] = DRV8833(in1, in2, pwm=use_pwm)
        self.use_pwm = use_pwm

    def all_forward(self, speed=None):
        for m in self.motors.values():
            if self.use_pwm and speed is not None:
                m.forward(speed)
            else:
                m.forward()

    def all_brake(self):
        for m in self.motors.values():
            m.brake()

    def all_coast(self):
        for m in self.motors.values():
            m.coast()

    def all_reverse(self, speed=None):  # probably unused for props, but provided
        for m in self.motors.values():
            if self.use_pwm and speed is not None:
                m.reverse(speed)
            else:
                m.reverse()

    def each(self):
        for name, m in self.motors.items():
            yield name, m

def ramp(group, start, end, duration, steps):
    if duration <= 0 or steps <= 0:
        group.all_forward(end)
        return
    step_time = duration / steps
    delta = (end - start) / steps
    current = start
    for _ in range(steps):
        group.all_forward(int(current))
        sleep(step_time)
        current += delta

def main():
    print("=== MOTOR TAKEOFF TEST ===")
    print("Configured motors:")
    for name, pins in MOTOR_PINS.items():
        print(f"  {name}: {pins}")
    if not MOTOR_PINS:
        print("No motors configured. Edit MOTOR_PINS list.")
        return
    group = MotorGroup(MOTOR_PINS, use_pwm=USE_PWM)

    # Countdown
    print("Safety countdown (ensure props removed!)")
    for i in range(3, 0, -1):
        print(i)
        sleep(1)
    print("Starting spin check...")

    try:
        if USE_PWM:
            # Individual spin test at low speed
            print("Individual spin + direction check (low duty)")
            for name, m in group.each():
                print(f" {name} forward...")
                m.forward(SPIN_CHECK_SPEED)
                sleep(1)
                m.brake()
                sleep(0.25)
                print(f" {name} reverse (brief)...")
                m.reverse(SPIN_CHECK_SPEED)
                sleep(1)
                m.brake()
                sleep(0.25)
            print("(Verify physical rotation directions now; swap A/B leads or pin order if needed.)")
            print("Collective ramp to target")
            ramp(group, 0, SPIN_CHECK_SPEED, 0.5, int(RAMP_STEPS/2))
            ramp(group, SPIN_CHECK_SPEED, TARGET_SPEED, RAMP_UP_TIME, RAMP_STEPS)
            print("Hold at target")
            group.all_forward(TARGET_SPEED)
            sleep(HOLD_TIME)
            print("Ramp down")
            ramp(group, TARGET_SPEED, 0, RAMP_DOWN_TIME, RAMP_STEPS)
        else:
            print("Full ON (no PWM mode)")
            group.all_forward()
            sleep(HOLD_TIME)
            print("Brake")
            group.all_brake()
            sleep(0.5)
            print("Coast")
            group.all_coast()
        print("Test complete. Motors stopped.")
    except KeyboardInterrupt:
        print("\nAbort: Braking motors.")
        group.all_brake()
        sleep(0.5)
        group.all_coast()
    except Exception as e:
        print("Error during test:", e)
        print("Applying brake.")
        group.all_brake()
        sleep(0.5)
        group.all_coast()

if __name__ == "__main__":
    main()
