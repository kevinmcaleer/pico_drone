from machine import I2C, Pin
import time

# Set up I2C0 using GPIO0 (SDA) and GPIO1 (SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

print("Scanning I2C bus...")

while True:
    devices = i2c.scan()
    
    if devices:
        print("I2C device(s) found at address(es):")
        for device in devices:
            print(" - 0x{:02X}".format(device))
    else:
        print("No I2C devices found.")
    
    time.sleep(2)
