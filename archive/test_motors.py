# Test Motors

from machine import Pin
from time import sleep

# Define IN3 and IN4
in3 = Pin(2, Pin.OUT)
in4 = Pin(3, Pin.OUT)

print("Starting DRV8833 IN3/IN4 test...")

try:
    while True:
        # Rotate forward
        print("Forward")
        in3.high()
        in4.low()
        sleep(1)

        # Brake
        print("Brake")
        in3.high()
        in4.high()
        sleep(1)

        # Reverse
        print("Reverse")
        in3.low()
        in4.high()
        sleep(1)

        # Coast
        print("Coast")
        in3.low()
        in4.low()
        sleep(1)

except KeyboardInterrupt:
    print("Test stopped.")
    in3.low()
    in4.low()
