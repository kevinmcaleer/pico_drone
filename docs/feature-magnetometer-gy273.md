# Feature: Magnetometer (GY-273) Integration

## Description

Integrate the GY-273 magnetometer sensor with the Raspberry Pi Pico 2W flight computer using MicroPython. This feature will provide heading information for navigation and orientation correction.

## Acceptance Criteria

- The GY-273 magnetometer is connected via I2C and successfully communicates with the Pico.
- Sensor data (magnetic field strength in X, Y, Z axes) is read and processed.
- Heading is calculated and available for use by the flight control system.
- Errors in sensor communication are handled gracefully.

## Related Epic

- Build the Flight Computer for MicroPython Powered Drone

## Test Coverage

- Unit tests for sensor reading functions
- Integration test for end-to-end data acquisition and heading calculation
