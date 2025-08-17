#!/bin/bash
# cli-add-issues.sh
# Add all epics, features, and stories as GitHub issues with appropriate labels

REPO="kevinmcaleer/pico_drone"

# Epic
hub issue create -r $REPO -t "Epic: Build the Flight Computer for MicroPython Powered Drone" -F docs/epic-flight-computer.md -l epic

# Feature

# IMU Feature
hub issue create -r $REPO -t "Feature: IMU (GY-91) Integration" -F docs/feature-imu-gy91.md -l feature

# Stories

# IMU Stories
hub issue create -r $REPO -t "Story: Connect GY-91 IMU via I2C" -b "As a developer, I want to connect the GY-91 IMU to the Pico via I2C so that I can read sensor data\n\nAcceptance Criteria:\n- The Pico can detect the GY-91 on the I2C bus.\n- Communication errors are logged and handled." -l story
hub issue create -r $REPO -t "Story: Read IMU sensor data" -b "As a developer, I want to read acceleration, gyroscope, and temperature data from the GY-91 so that I can use it for flight stabilization\n\nAcceptance Criteria:\n- Raw sensor data is read and output for debugging.\n- Data is available at a regular interval (e.g., 10Hz)." -l story
hub issue create -r $REPO -t "Story: Process IMU data with Madgwick filter" -b "As a developer, I want to process IMU data using a Madgwick filter so that I can obtain orientation (pitch and roll)\n\nAcceptance Criteria:\n- The Madgwick filter is implemented and tested with sample data.\n- Orientation data is output and available for flight control." -l story
hub issue create -r $REPO -t "Story: Handle sensor errors gracefully (IMU)" -b "As a developer, I want to handle sensor errors gracefully so that the flight computer remains robust\n\nAcceptance Criteria:\n- Sensor read failures do not crash the system.\n- Errors are logged and retried." -l story

# Magnetometer Feature
hub issue create -r $REPO -t "Feature: Magnetometer (GY-273) Integration" -F docs/feature-magnetometer-gy273.md -l feature

# Magnetometer Stories
hub issue create -r $REPO -t "Story: Connect GY-273 magnetometer via I2C" -b "As a developer, I want to connect the GY-273 magnetometer to the Pico via I2C so that I can read magnetic field data\n\nAcceptance Criteria:\n- The Pico can detect the GY-273 on the I2C bus.\n- Communication errors are logged and handled." -l story
hub issue create -r $REPO -t "Story: Read magnetometer sensor data" -b "As a developer, I want to read X, Y, Z magnetic field data from the GY-273 so that I can use it for heading calculation\n\nAcceptance Criteria:\n- Raw sensor data is read and output for debugging.\n- Data is available at a regular interval (e.g., 10Hz)." -l story
hub issue create -r $REPO -t "Story: Calculate heading from magnetometer data" -b "As a developer, I want to calculate heading from the magnetometer data so that the drone can determine its orientation\n\nAcceptance Criteria:\n- Heading is calculated from X, Y, Z data.\n- Heading is output and available for flight control." -l story
hub issue create -r $REPO -t "Story: Handle sensor errors gracefully (magnetometer)" -b "As a developer, I want to handle sensor errors gracefully so that the flight computer remains robust\n\nAcceptance Criteria:\n- Sensor read failures do not crash the system.\n- Errors are logged and retried." -l story

# GPS Feature
hub issue create -r $REPO -t "Feature: GPS (NEO-6M Compatible) Integration" -F docs/feature-gps-neo6m.md -l feature

# GPS Stories
hub issue create -r $REPO -t "Story: Connect NEO-6M GPS via UART" -b "As a developer, I want to connect the NEO-6M GPS module to the Pico via UART so that I can receive GPS data\n\nAcceptance Criteria:\n- The Pico can detect and communicate with the GPS module over UART.\n- Communication errors are logged and handled." -l story
hub issue create -r $REPO -t "Story: Parse GPS data" -b "As a developer, I want to parse latitude, longitude, altitude, speed, and time from the GPS data so that I can use it for navigation\n\nAcceptance Criteria:\n- GPS data is parsed and output for debugging.\n- Data is available at a regular interval (e.g., 1Hz)." -l story
hub issue create -r $REPO -t "Story: Make GPS data available to flight control" -b "As a developer, I want to make GPS location data available to the flight control system so that the drone can use it for navigation and telemetry\n\nAcceptance Criteria:\n- Location data is accessible by other modules.\n- Data is updated in real time." -l story
hub issue create -r $REPO -t "Story: Handle GPS errors gracefully" -b "As a developer, I want to handle GPS errors gracefully so that the flight computer remains robust\n\nAcceptance Criteria:\n- GPS read failures do not crash the system.\n- Errors are logged and retried." -l story
