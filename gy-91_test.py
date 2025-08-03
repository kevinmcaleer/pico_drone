# GY-91 Test
from machine import I2C, Pin
import time

# I2C Addresses
MPU9250_ADDR = 0x68
BMP280_ADDR = 0x76  # Sometimes 0x77

# MPU-9250 Registers
MPU_WHO_AM_I = 0x75

# BMP280 Registers
BMP280_ID_REG = 0xD0

# Set up I2C – adjust pins to match your board
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # For Raspberry Pi Pico
# i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)  # For ESP32

def scan_i2c():
    print("Scanning I2C bus...")
    devices = i2c.scan()
    if devices:
        for d in devices:
            print("Found device at: 0x{:02X}".format(d))
    else:
        print("No I2C devices found.")

def check_mpu9250():
    try:
        whoami = i2c.readfrom_mem(MPU9250_ADDR, MPU_WHO_AM_I, 1)[0]
        print("MPU-9250 WHO_AM_I: 0x{:02X}".format(whoami))
        if whoami == 0x71:
            print("MPU-9250 detected successfully.")
        else:
            print("Unexpected WHO_AM_I from MPU-9250.")
    except Exception as e:
        print("Failed to communicate with MPU-9250:", e)

def check_bmp280():
    try:
        chip_id = i2c.readfrom_mem(BMP280_ADDR, BMP280_ID_REG, 1)[0]
        print("BMP280 ID: 0x{:02X}".format(chip_id))
        if chip_id in [0x58, 0x56, 0x57]:  # 0x58 for BMP280, others for BME280
            print("BMP280 detected successfully.")
        else:
            print("Unexpected ID for BMP280.")
    except Exception as e:
        print("Failed to communicate with BMP280:", e)

# Run tests
scan_i2c()
check_mpu9250()
check_bmp280()
