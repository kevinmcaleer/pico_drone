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
- `scripts/` — Shell scripts for deployment and GitHub automation
- `gamepad.py`, `ssd1306.py` — Bluetooth gamepad and OLED display drivers for Pico


## Features & Progress

- [x] Project structure and documentation folders created
- [x] Epic and feature breakdown for IMU, Magnetometer, and GPS
- [x] User stories and test skeletons for each feature
- [x] CLI script to add all epics, features, and stories as GitHub issues with correct labels



## How to Use

- Run `scripts/cli-add-issues.sh` to create all project issues on GitHub (requires GitHub CLI `gh`)
- Add new features, user stories, and tests as the project evolves

### Deploying to the Pico

1. Connect your Raspberry Pi Pico to your computer and mount it (it should appear as a USB drive, e.g., `/media/$USER/RPI-RP2` on Linux, or a similar path on macOS/Windows).
2. Run the deployment script:

  ```sh
  scripts/deploy_to_pico.sh <PICO_MOUNT_PATH>
  ```
  Replace `<PICO_MOUNT_PATH>` with the actual mount path of your Pico. If omitted, the script will try a default path.
3. This will copy all required files (`flight_computer.py`, `imu_gy91.py`, `mag_gy273.py`, `gps_neo6m.py`, `gamepad.py`, `ssd1306.py`) to your Pico.
4. Eject/unmount the Pico and reboot it to run the flight computer.


## Contributing

Contributions are welcome! Please open issues or pull requests for new features, bug fixes, or improvements.


---

*This project is a work in progress and will be updated as development continues.*
