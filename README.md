# Pico Drone Flight Computer

This project is building a MicroPython-powered flight computer for a drone using the Raspberry Pi Pico 2W. The system integrates multiple sensors and modules to provide real-time flight control, navigation, and safety features.

## Overview

- **Flight Computer:** Raspberry Pi Pico 2W running MicroPython
- **Sensors:**
  - IMU: GY-91 (accelerometer, gyroscope, barometer)
  - Magnetometer: GY-273
  - GPS: NEO-6M compatible
- **Motor Control:** Two DRV8833 motor drivers
- **Control:** Bluetooth gamepad
- **Safety:**
  - Drone stops and hovers if Bluetooth connection drops
  - Automatic reconnection attempts


## Project Structure

- `docs/` — Epics, features, and user stories
- `tests/` — Test scripts for each feature
- `design/` — Design documentation
- `archive/` — Early experiments and legacy scripts


## Features & Progress

- [x] Project structure and documentation folders created
- [x] Epic and feature breakdown for IMU, Magnetometer, and GPS
- [x] User stories and test skeletons for each feature
- [x] CLI script to add all epics, features, and stories as GitHub issues with correct labels


## How to Use

- Run `cli-add-issues.sh` to create all project issues on GitHub (requires GitHub CLI `gh`)
- Add new features, user stories, and tests as the project evolves


## Contributing

Contributions are welcome! Please open issues or pull requests for new features, bug fixes, or improvements.


---

*This project is a work in progress and will be updated as development continues.*
