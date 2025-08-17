from machine import I2C, Pin
import time
import struct

# QMC5883L default I2C address
QMC5883L_ADDR = 0x0D

# Initialize I2C (I2C0 on GPIO0=SDA, GPIO1=SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

print(i2c.scan())

# QMC5883L register addresses
REG_CONTROL = 0x09
REG_DATA = 0x00

# Control register setup:
#   OSR = 512, RNG = 8G, ODR = 50Hz, MODE = continuous
control_byte = 0b00011101  # OSR=512, Range=8G, ODR=50Hz, Continuous mode

# Write to control register
i2c.writeto_mem(QMC5883L_ADDR, REG_CONTROL, bytes([control_byte]))

print("QMC5883L initialized at address 0x0D")

# Function to read X, Y, Z values
def read_qmc5883l():
    try:
        data = i2c.readfrom_mem(QMC5883L_ADDR, REG_DATA, 6)
        x = struct.unpack('<h', data[0:2])[0]
        y = struct.unpack('<h', data[2:4])[0]
        z = struct.unpack('<h', data[4:6])[0]
        return x, y, z
    except Exception as e:
        print("Read error:", e)
        return None, None, None

# Main loop
while True:
    x, y, z = read_qmc5883l()
    if x is not None:
        print("X: {:>6}  Y: {:>6}  Z: {:>6}".format(x, y, z))
    time.sleep(1)
