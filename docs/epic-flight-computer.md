# Epic: Build the Flight Computer for MicroPython Powered Drone

## Overview

We will build a flight computer for our drone using a Raspberry Pi Pico 2W. The system will be powered by MicroPython and will integrate the following sensors and components:

### Sensors

- **IMU:** GY-91
- **Magnetometer:** GY-273
- **GPS:** NEO-6M compatible


### Motor Control

- **ESC:** Two DRV8833 motor drivers


### Control

- The drone will be controlled using a Bluetooth gamepad.


## Safety Features

- The drone must stop and hover in place if the Bluetooth connection drops.
- The system should attempt to reconnect automatically if the connection is lost.


---

This epic will be broken down into features and user stories in subsequent documentation.
