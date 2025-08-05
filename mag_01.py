from machine import Pin, I2C
import time

# I2C setup (adjust pins for your board)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

MPU9250_ADDR = 0x68
AK8963_ADDR = 0x0C

# MPU9250 Register Map
INT_PIN_CFG = 0x37
PWR_MGMT_1 = 0x6B

# Magnetometer Register Map
AK8963_WHO_AM_I = 0x00
AK8963_CNTL1 = 0x0A
AK8963_STATUS1 = 0x02
AK8963_HXL = 0x03

def init_magnetometer():
    # Wake MPU-9250
    write_i2c(MPU9250_ADDR, PWR_MGMT_1, 0x00)
    time.sleep_ms(100)

    # Enable bypass to talk directly to AK8963
    write_i2c(MPU9250_ADDR, INT_PIN_CFG, 0x02)
    time.sleep_ms(10)

    # Verify AK8963 is connected
    who_am_i = read_i2c(AK8963_ADDR, 0x00)[0]
    if who_am_i != 0x48:
        raise Exception(f"AK8963 not found! WHO_AM_I={hex(who_am_i)}")

    # Set to continuous mode 2 (100 Hz)
    write_i2c(AK8963_ADDR, 0x0A, 0x06)
    time.sleep_ms(10)


def write_i2c(addr, reg, data):
    i2c.writeto_mem(addr, reg, bytes([data]))

def read_i2c(addr, reg, n=1):
    return i2c.readfrom_mem(addr, reg, n)


def read_magnetometer():
    status = read_i2c(AK8963_ADDR, AK8963_STATUS1)[0]
    if not (status & 0x01):
        return None  # Data not ready

    data = read_i2c(AK8963_ADDR, AK8963_HXL, 6)
    x = int.from_bytes(data[0:2], 'little', signed=True)
    y = int.from_bytes(data[2:4], 'little', signed=True)
    z = int.from_bytes(data[4:6], 'little', signed=True)
    return x, y, z

# Main
init_magnetometer()
print("Reading AK8963 magnetometer...")

while True:
    mag = read_magnetometer()
    if mag:
        print("Magnetometer:", mag)
    time.sleep(0.5)
