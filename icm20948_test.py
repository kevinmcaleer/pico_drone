from machine import I2C, Pin
import time

# ICM-20948 I2C address (can be 0x68 or 0x69 depending on AD0 pin)
ICM20948_ADDR = 0x68
REG_WHO_AM_I = 0x00  # WHO_AM_I register

# Set up I2C – change pins as needed
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)  # For Pico
# i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)  # For ESP32

def scan_i2c():
    print("Scanning I2C bus...")
    devices = i2c.scan()
    if devices:
        for dev in devices:
            print("I2C device found at address: 0x{:02X}".format(dev))
    else:
        print("No I2C devices found.")

def read_who_am_i():
    try:
        val = i2c.readfrom_mem(ICM20948_ADDR, REG_WHO_AM_I, 1)[0]
        print("ICM-20948 WHO_AM_I: 0x{:02X}".format(val))
        if val == 0xEA:
            print("ICM-20948 detected successfully.")
        else:
            print("Unexpected WHO_AM_I value.")
    except Exception as e:
        print("Error reading WHO_AM_I:", e)

scan_i2c()
read_who_am_i()
