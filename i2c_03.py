from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
try:
    whoami = i2c.readfrom_mem(0x0C, 0x00, 1)[0]
    print("AK8963 WHO_AM_I:", hex(whoami))
except Exception as e:
    print("Read failed:", e)
