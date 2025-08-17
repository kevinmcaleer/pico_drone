#!/bin/bash
# cli-add-issues.sh
# Add all epics, features, and stories as GitHub issues with appropriate labels

REPO="kevinmcaleer/pico_drone"

# Epic
hub issue create -r $REPO -t "Epic: Build the Flight Computer for MicroPython Powered Drone" -F docs/epic-flight-computer.md -l epic

# Feature
hub issue create -r $REPO -t "Feature: IMU (GY-91) Integration" -F docs/feature-imu-gy91.md -l feature

# Stories
hub issue create -r $REPO -t "Story: Connect GY-91 IMU via I2C" -b "As a developer, I want to connect the GY-91 IMU to the Pico via I2C so that I can read sensor data\n\nAcceptance Criteria:\n- The Pico can detect the GY-91 on the I2C bus.\n- Communication errors are logged and handled." -l story

hub issue create -r $REPO -t "Story: Read IMU sensor data" -b "As a developer, I want to read acceleration, gyroscope, and temperature data from the GY-91 so that I can use it for flight stabilization\n\nAcceptance Criteria:\n- Raw sensor data is read and output for debugging.\n- Data is available at a regular interval (e.g., 10Hz)." -l story

hub issue create -r $REPO -t "Story: Process IMU data with Madgwick filter" -b "As a developer, I want to process IMU data using a Madgwick filter so that I can obtain orientation (pitch and roll)\n\nAcceptance Criteria:\n- The Madgwick filter is implemented and tested with sample data.\n- Orientation data is output and available for flight control." -l story

hub issue create -r $REPO -t "Story: Handle sensor errors gracefully" -b "As a developer, I want to handle sensor errors gracefully so that the flight computer remains robust\n\nAcceptance Criteria:\n- Sensor read failures do not crash the system.\n- Errors are logged and retried." -l story
