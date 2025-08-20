"""
test_motor_takeoff.py

Two-chip DRV8833 motor takeoff style test.
Supports 4 brushed motors (two per DRV8833 chip: channels A & B).

Now uses DRV8833Chip (4 inputs per chip) instead of one DRV8833 instance per motor.

SAFETY:
 - REMOVE PROPS for initial testing.
 - Secure frame; have power cutoff ready.
 - Verify rotation directions BEFORE adding props (CW/CCW per quad layout).

WIRING ASSUMPTION:
 You have up to 2 DRV8833 breakout boards. Each exposes AIN1, AIN2, BIN1, BIN2.
 We map logical motor names to (chip_index, channel, desired_rotation_sign).
 Channel is 'A' or 'B'. Rotation sign (1 or -1) lets you invert without rewiring.

EDIT THESE:
 - CHIP_PINS: list of dicts each with keys 'AIN1','AIN2','BIN1','BIN2'. Pin numbers are Pico GPIOs.
 - MOTOR_MAP: map logical name -> { 'chip':0|1, 'ch':'A'|'B', 'dir':1|-1 }
 - Speeds & timing constants below.

USAGE:
 import test_motor_takeoff  (auto-runs main when __name__ == '__main__')
 or run main() manually.
"""
from time import sleep

from drv8833 import DRV8833Chip

# ---------------- Configuration -----------------
# List one entry per DRV8833 chip you actually wired.
# Example placeholder pins (replace with real wiring):
CHIP_PINS = [
    { 'AIN1':2, 'AIN2':3, 'BIN1':4, 'BIN2':5 },  # Chip 0
    { 'AIN1':6, 'AIN2':7, 'BIN1':8, 'BIN2':9 },  # Chip 1
]

# Logical motor mapping. Names should match frame corners.
# dir: +1 means forward() should spin the motor in the desired thrust direction.
#      -1 means reversed wiring; we flip commands internally.
MOTOR_MAP = {
    'top_left':     { 'chip':0, 'ch':'A', 'dir': 1 },
    'bottom_left':  { 'chip':0, 'ch':'B', 'dir': 1 },
    'top_right':    { 'chip':1, 'ch':'A', 'dir': 1 },
    'bottom_right': { 'chip':1, 'ch':'B', 'dir': 1 },
}

USE_PWM = True            # Always True for variable thrust
SPIN_CHECK_SPEED = 14000  # Low duty for spin verification
TARGET_SPEED = 40000      # Adjust for hover test
RAMP_UP_TIME = 1.0
HOLD_TIME = 2.0
RAMP_DOWN_TIME = 1.0
RAMP_STEPS = 20

# ------------------------------------------------

class Fleet:
    def __init__(self, chip_pins, motor_map, use_pwm=True):
        self.chips = []
        for cfg in chip_pins:
            chip = DRV8833Chip(cfg['AIN1'], cfg['AIN2'], cfg['BIN1'], cfg['BIN2'], pwm=use_pwm)
            self.chips.append(chip)
        self.map = motor_map
        self.use_pwm = use_pwm

    def _channel(self, name):
        info = self.map[name]
        chip = self.chips[info['chip']]
        ch = chip.motor_a if info['ch'] in ('A','a') else chip.motor_b
        return ch, info['dir']

    def set_motor(self, name, duty):
        ch, sign = self._channel(name)
        duty = int(duty)
        if sign >= 0:
            if duty >= 0:
                ch.forward(duty)
            else:
                ch.reverse(-duty)
        else:
            if duty >= 0:
                ch.reverse(duty)
            else:
                ch.forward(-duty)

    def brake_all(self):
        for chip in self.chips:
            chip.motor_a.brake()
            chip.motor_b.brake()

    def coast_all(self):
        for chip in self.chips:
            chip.motor_a.coast()
            chip.motor_b.coast()

    def all(self):
        for name in self.map.keys():
            yield name

    def set_all(self, duty):
        for name in self.all():
            self.set_motor(name, duty)


def ramp(fleet, start, end, duration, steps):
    if duration <= 0 or steps <= 0:
        fleet.set_all(end)
        return
    step_time = duration / steps
    delta = (end - start) / steps
    current = start
    for _ in range(steps):
        fleet.set_all(int(current))
        sleep(step_time)
        current += delta


def individual_spin_test(fleet, speed):
    print('Individual spin & direction check:')
    for name in fleet.all():
        print(f' {name} forward...')
        fleet.set_motor(name, speed)
        sleep(1)
        fleet.brake_all()
        sleep(0.2)
        print(f' {name} reverse...')
        fleet.set_motor(name, -speed)
        sleep(1)
        fleet.brake_all()
        sleep(0.2)
    print('Verify physical rotation; adjust MOTOR_MAP dir or swap pins if wrong.')


def main():
    print('=== TEST MOTOR TAKEOFF (DRV8833Chip) ===')
    print('Chips configured:')
    for idx, cfg in enumerate(CHIP_PINS):
        print(f' Chip {idx}: AIN1={cfg["AIN1"]} AIN2={cfg["AIN2"]} BIN1={cfg["BIN1"]} BIN2={cfg["BIN2"]}')
    print('Motors:')
    for name, info in MOTOR_MAP.items():
        print(f' {name}: chip={info["chip"]} ch={info["ch"]} dir={info["dir"]}')

    fleet = Fleet(CHIP_PINS, MOTOR_MAP, use_pwm=USE_PWM)

    print('Safety countdown (props off!)')
    for i in range(3,0,-1):
        print(i)
        sleep(1)

    try:
        if USE_PWM:
            individual_spin_test(fleet, SPIN_CHECK_SPEED)
            print('Collective ramp')
            ramp(fleet, 0, SPIN_CHECK_SPEED, 0.5, int(RAMP_STEPS/2))
            ramp(fleet, SPIN_CHECK_SPEED, TARGET_SPEED, RAMP_UP_TIME, RAMP_STEPS)
            print('Hold at target')
            fleet.set_all(TARGET_SPEED)
            sleep(HOLD_TIME)
            print('Ramp down')
            ramp(fleet, TARGET_SPEED, 0, RAMP_DOWN_TIME, RAMP_STEPS)
        else:
            print('PWM disabled path (full on / off)')
            fleet.set_all(65535)
            sleep(HOLD_TIME)
            fleet.brake_all()
            sleep(0.3)
            fleet.coast_all()
        print('Test complete.')
    except KeyboardInterrupt:
        print('\nAbort: braking.')
    except Exception as e:
        print('Error:', e)
    finally:
        # Ensure motors are not left running
        fleet.brake_all()
        sleep(0.4)
        fleet.coast_all()

if __name__ == '__main__':
    main()
