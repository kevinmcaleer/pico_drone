from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

MPU9250_ADDR = 0x68
BMP280_ADDR = 0x76

def scan_i2c():
    print("Scanning I2C...")
    for addr in i2c.scan():
        print("Found device at 0x{:02X}".format(addr))

def read_register(addr, reg, nbytes=1):
    try:
        i2c.writeto(addr, bytes([reg]))
        return i2c.readfrom(addr, nbytes)
    except Exception as e:
        print("Error reading from 0x{:02X} reg 0x{:02X}:".format(addr, reg), e)
        return None

# WHO_AM_I Registers
MPU_WHO_AM_I = 0x75
BMP280_ID_REG = 0xD0

scan_i2c()

# i2c.writeto(0x76, b'\xD0')  # BMP280 chip ID
# print(i2c.readfrom(0x76, 1))

try:
    i2c.writeto_mem(0x68, 0x6B, b'\x00')
    print("MPU-9250 woken up.")
except Exception as e:
    print("Failed to wake MPU-9250:", e)

# Test MPU-9250
data = read_register(MPU9250_ADDR, MPU_WHO_AM_I)
if data:
    print("MPU-9250 WHO_AM_I: 0x{:02X}".format(data[0]))

# Test BMP280
data = read_register(BMP280_ADDR, BMP280_ID_REG)
if data:
    print("BMP280 ID: 0x{:02X}".format(data[0]))
