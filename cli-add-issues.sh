#!/bin/bash
# cli-add-issues.sh
# Add all epics, features, and stories as GitHub issues with appropriate labels using gh CLI

REPO="kevinmcaleer/pico_drone"

# Epic
gh issue create --repo $REPO --title "Epic: Build the Flight Computer for MicroPython Powered Drone" --body-file docs/epic-flight-computer.md --label epic

# IMU Feature
gh issue create --repo $REPO --title "Feature: IMU (GY-91) Integration" --body-file docs/feature-imu-gy91.md --label feature

# IMU Stories
gh issue create --repo $REPO --title "Story: Connect GY-91 IMU via I2C" --body "As a developer, I want to connect the GY-91 IMU to the Pico via I2C so that I can read sensor data

Acceptance Criteria:
- The Pico can detect the GY-91 on the I2C bus.
- Communication errors are logged and handled." --label story
gh issue create --repo $REPO --title "Story: Read IMU sensor data" --body "As a developer, I want to read acceleration, gyroscope, and temperature data from the GY-91 so that I can use it for flight stabilization

Acceptance Criteria:
- Raw sensor data is read and output for debugging.
- Data is available at a regular interval (e.g., 10Hz)." --label story
gh issue create --repo $REPO --title "Story: Process IMU data with Madgwick filter" --body "As a developer, I want to process IMU data using a Madgwick filter so that I can obtain orientation (pitch and roll)

Acceptance Criteria:
- The Madgwick filter is implemented and tested with sample data.
- Orientation data is output and available for flight control." --label story
gh issue create --repo $REPO --title "Story: Handle sensor errors gracefully (IMU)" --body "As a developer, I want to handle sensor errors gracefully so that the flight computer remains robust

Acceptance Criteria:
- Sensor read failures do not crash the system.
- Errors are logged and retried." --label story

# Magnetometer Feature
gh issue create --repo $REPO --title "Feature: Magnetometer (GY-273) Integration" --body-file docs/feature-magnetometer-gy273.md --label feature

# Magnetometer Stories
gh issue create --repo $REPO --title "Story: Connect GY-273 magnetometer via I2C" --body "As a developer, I want to connect the GY-273 magnetometer to the Pico via I2C so that I can read magnetic field data

Acceptance Criteria:
- The Pico can detect the GY-273 on the I2C bus.
- Communication errors are logged and handled." --label story
gh issue create --repo $REPO --title "Story: Read magnetometer sensor data" --body "As a developer, I want to read X, Y, Z magnetic field data from the GY-273 so that I can use it for heading calculation

Acceptance Criteria:
- Raw sensor data is read and output for debugging.
- Data is available at a regular interval (e.g., 10Hz)." --label story
gh issue create --repo $REPO --title "Story: Calculate heading from magnetometer data" --body "As a developer, I want to calculate heading from the magnetometer data so that the drone can determine its orientation

Acceptance Criteria:
- Heading is calculated from X, Y, Z data.
- Heading is output and available for flight control." --label story
gh issue create --repo $REPO --title "Story: Handle sensor errors gracefully (magnetometer)" --body "As a developer, I want to handle sensor errors gracefully so that the flight computer remains robust

Acceptance Criteria:
- Sensor read failures do not crash the system.
- Errors are logged and retried." --label story

# GPS Feature
gh issue create --repo $REPO --title "Feature: GPS (NEO-6M Compatible) Integration" --body-file docs/feature-gps-neo6m.md --label feature

# GPS Stories
gh issue create --repo $REPO --title "Story: Connect NEO-6M GPS via UART" --body "As a developer, I want to connect the NEO-6M GPS module to the Pico via UART so that I can receive GPS data

Acceptance Criteria:
- The Pico can detect and communicate with the GPS module over UART.
- Communication errors are logged and handled." --label story
gh issue create --repo $REPO --title "Story: Parse GPS data" --body "As a developer, I want to parse latitude, longitude, altitude, speed, and time from the GPS data so that I can use it for navigation

Acceptance Criteria:
- GPS data is parsed and output for debugging.
- Data is available at a regular interval (e.g., 1Hz)." --label story
gh issue create --repo $REPO --title "Story: Make GPS data available to flight control" --body "As a developer, I want to make GPS location data available to the flight control system so that the drone can use it for navigation and telemetry

Acceptance Criteria:
- Location data is accessible by other modules.
- Data is updated in real time." --label story
gh issue create --repo $REPO --title "Story: Handle GPS errors gracefully" --body "As a developer, I want to handle GPS errors gracefully so that the flight computer remains robust

Acceptance Criteria:
- GPS read failures do not crash the system.
- Errors are logged and retried." --label story