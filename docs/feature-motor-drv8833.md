# Feature: Motor Control (DRV8833) Integration

## Description

Integrate dual DRV8833 motor drivers with the Raspberry Pi Pico 2W flight computer using MicroPython. This feature provides bidirectional speed control for multiple brushed DC motors (or paired as differential thrust units) using PWM and supports braking, coasting, and safety failsafes.

## Acceptance Criteria

- Two DRV8833 boards (or both channels on one board) are wired and initialized successfully.
- Each motor supports: forward, reverse, brake, coast, and variable speed via PWM (0–100%).
- A unified motor control interface exposes simple methods (e.g. `set_motor(id, speed)` where speed ∈ [-1.0, 1.0]).
- Failsafe logic: motors immediately stop (brake or coast as configured) on:
  - Gamepad/Bluetooth disconnect
  - Sensor critical failure (IMU orientation invalid, runaway values)
  - Explicit emergency stop command
- Optional ramping/acceleration limiting to prevent sudden current spikes.
- Motor status (commanded speed, last update timestamp, fault flags) available to flight computer.
- Errors (e.g., invalid motor ID, out-of-range speed) are handled gracefully without crashing.

## Related Epic

- Build the Flight Computer for MicroPython Powered Drone

## Dependencies / Inputs

- `drv8833.py` module (low-level driver)
- Flight computer loop (`flight_computer.py`)
- Gamepad input module for throttle/command mapping
- IMU & failsafe signaling

## Test Coverage

- Unit tests for `drv8833.py` (already implemented) extended to cover ramping (if added) and error paths.
- New tests for a higher-level motor manager abstraction:
  - Speed normalization & clamping
  - Direction mapping correctness
  - Failsafe trigger stops all motors
  - Ramping / rate limiting (if implemented)
- Integration test: simulated gamepad input -> motor command translation.

## Non-Goals (Initial Phase)

- Closed-loop RPM or position feedback (no encoders assumed yet)
- Current sensing or thermal monitoring
- Advanced mixing (yaw/pitch stabilization) – deferred to flight control logic

## Notes

Start simple with direct mapping, then iterate to add safety layers and smoothing once baseline control is verified on bench.
