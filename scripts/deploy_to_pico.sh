#!/bin/bash
# deploy_to_pico.sh
# Copy all required files to the Raspberry Pi Pico using rshell
# Usage: ./deploy_to_pico.sh <PICO_MOUNT_PATH>

PICO_MOUNT=${1:-/media/$USER/RPI-RP2}

FILES="flight_computer.py imu_gy91.py mag_gy273.py gps_neo6m.py gamepad.py ssd1306.py"

for file in $FILES; do
    echo "Copying $file to $PICO_MOUNT..."
    cp $file $PICO_MOUNT/
done

echo "Deployment complete."
