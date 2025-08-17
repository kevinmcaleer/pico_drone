# Feature: GPS (NEO-6M Compatible) Integration

## Description

Integrate a NEO-6M compatible GPS module with the Raspberry Pi Pico 2W flight computer using MicroPython. This feature will provide real-time location, speed, and time data for navigation and telemetry.

## Acceptance Criteria

- The GPS module is connected via UART and successfully communicates with the Pico.
- GPS data (latitude, longitude, altitude, speed, time) is read and parsed.
- Location data is available for use by the flight control system.
- Errors in GPS communication are handled gracefully.

## Related Epic

- Build the Flight Computer for MicroPython Powered Drone

## Test Coverage

- Unit tests for GPS data parsing functions
- Integration test for end-to-end data acquisition and parsing
