# Epic 

Build the flight computer for our micropython powered drone. it will use a Raspberry Pi Pico 2W for the flight computer and has the following sensors:

- IMU - GY-91
- Magnetometer - GY-273
- GPS - NEO-6M compatible

For ESC, the drone will use two DRV8833 motor drivers.

The drone will be controlled using a bluetooth gamepad.

We want to include safety features such as stopping the drone and hovering in place if the bluetooth connection drops (and reconnecting automatically).
