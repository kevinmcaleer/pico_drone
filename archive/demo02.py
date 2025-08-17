from micropyGPS import MicropyGPS
from machine import UART
import time

# === Adjust UART pin numbers below to match your board and wiring ===
uart = UART(1, baudrate=9600, tx=4, rx=5)  # For ESP32
# uart = UART(1, baudrate=9600, tx=4, rx=5)  # For Raspberry Pi Pico

gps = MicropyGPS(location_formatting='dd')

last_print = time.ticks_ms()

while True:
    while uart.any():
        try:
            gps.update(uart.read(1).decode('utf-8'))
        except:
            print("error")
            pass  # In case of decoding errors

    # Print once per second
    if time.ticks_diff(time.ticks_ms(), last_print) > 1000:
        last_print = time.ticks_ms()
        if gps.latitude and gps.longitude:
            print("Latitude:", gps.latitude_string())
            print("Longitude:", gps.longitude_string())
            print("Satellites:", gps.satellites_in_use)
            print("UTC Time:", gps.timestamp)
            print("Date:", gps.date_string('long'))
            print("Speed (knots):", gps.speed)
            print("Altitude:", gps.altitude)
            print()
