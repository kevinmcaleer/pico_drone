from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

def write(addr, reg, val):
    i2c.writeto_mem(addr, reg, bytes([val]))

def read(addr, reg, n=1):
    return i2c.readfrom_mem(addr, reg, n)

# Step 1: Wake up MPU-9250
write(0x68, 0x6B, 0x00)       # PWR_MGMT_1 = 0x00 (wake up)
time.sleep_ms(100)

# Step 2: Disable I2C Master mode
write(0x68, 0x6A, 0x00)       # USER_CTRL = 0x00
time.sleep_ms(10)

# Step 3: Enable bypass mode
write(0x68, 0x37, 0x02)       # INT_PIN_CFG = 0x02
time.sleep_ms(10)

# Step 4: Scan I2C
print("Scan after proper bypass:", [hex(a) for a in i2c.scan()])
