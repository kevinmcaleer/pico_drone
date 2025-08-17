# Documentation for Modular Sensor and Flight Computer Code

## Overview

The codebase is organized into modular Python files for each sensor and the main flight computer logic. This makes the codebase easier to maintain, test, and extend.

### Modules
- `imu_gy91.py`: GY-91 IMU sensor (accelerometer, gyroscope, barometer)
- `mag_gy273.py`: GY-273 magnetometer sensor
- `gps_neo6m.py`: NEO-6M compatible GPS module
- `drv8833.py`: DRV8833 motor driver (forward, reverse, brake, coast, PWM support)
- `flight_computer.py`: Main integration script for sensor fusion and control

### How to Use
- Import the relevant module in your MicroPython project.
- Each module provides a class for interacting with the hardware.
- The `flight_computer.py` script demonstrates how to integrate all sensors for a working flight computer.

### Testing
- Each module has a corresponding test file in `tests/` using dummy/mock classes for hardware interfaces.
- DRV8833 motor driver is fully unit tested for all control modes (forward, reverse, brake, coast, PWM).
- Run tests with `python3 -m unittest discover tests` (on a standard Python environment).

### Extending
- Add new modules for additional sensors or features as needed.
- Keep each hardware interface in its own file for clarity and maintainability.

---

*See the README.md for a project overview and structure.*
