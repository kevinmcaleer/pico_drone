# gy-91 data test
from machine import I2C, Pin
import time
import struct

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

MPU_ADDR = 0x68

# Wake up MPU-9250 if not already done
i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')  # PWR_MGMT_1

def read_raw_data():
    # Read 14 bytes: Accel (6) + Temp (2) + Gyro (6)
    raw = i2c.readfrom_mem(MPU_ADDR, 0x3B, 14)
    data = struct.unpack('>hhhhhhh', raw)  # Big-endian 16-bit signed
    accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z = data
    return {
        'accel': (accel_x, accel_y, accel_z),
        'gyro': (gyro_x, gyro_y, gyro_z),
        'temp_raw': temp
    }

def convert_temp(raw_temp):
    # From datasheet: Temp in °C = (raw / 333.87) + 21
    return raw_temp / 333.87 + 21

while True:
    sensor = read_raw_data()
    ax, ay, az = sensor['accel']
    gx, gy, gz = sensor['gyro']
    temp_c = convert_temp(sensor['temp_raw'])

    print("Accel: x={:6d} y={:6d} z={:6d}".format(ax, ay, az))
    print("Gyro:  x={:6d} y={:6d} z={:6d}".format(gx, gy, gz))
    print("Temp:  {:.2f} °C".format(temp_c))
    print("-" * 40)
    time.sleep(0.5)
