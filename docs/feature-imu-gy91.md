# Feature: IMU (GY-91) Integration

## Description

Integrate the GY-91 IMU sensor with the Raspberry Pi Pico 2W flight computer using MicroPython. This feature will provide real-time orientation and acceleration data for flight stabilization and control.


## Acceptance Criteria

- The GY-91 IMU is connected via I2C and successfully communicates with the Pico.
- Sensor data (acceleration, gyroscope, temperature, and optionally barometer) is read and processed.
- Orientation is calculated using a sensor fusion algorithm (e.g., Madgwick filter).
- Data is available for use by the flight control system.
- Errors in sensor communication are handled gracefully.


## Related Epic

- Build the Flight Computer for MicroPython Powered Drone


## Test Coverage

- Unit tests for sensor reading functions
- Integration test for end-to-end data acquisition and processing

