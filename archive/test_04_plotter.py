# GY-91 + MPU-9250 + AK8963 + Madgwick on Raspberry Pi Pico
# Full orientation estimation (pitch, roll, yaw) via I2C master mode
# Outputs Thonny plotter-friendly data: pitch, roll, yaw as CSV
# Also prints raw accel, gyro, and temperature data

from machine import Pin, I2C
import time, math, struct
from madgwick import MadgwickAHRS

# === I2C Setup ===
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # Updated to match working config

# === MPU-9250 Register Map ===
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
USER_CTRL = 0x6A
INT_PIN_CFG = 0x37
I2C_MST_CTRL = 0x24
I2C_SLV0_ADDR = 0x25
I2C_SLV0_REG = 0x26
I2C_SLV0_CTRL = 0x27
I2C_SLV0_DO = 0x63
I2C_SLV1_ADDR = 0x28
I2C_SLV1_REG = 0x29
I2C_SLV1_CTRL = 0x2A
I2C_SLV1_DO = 0x64
EXT_SENS_DATA_00 = 0x49
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
TEMP_OUT_H = 0x41

# === AK8963 Register Map ===
AK8963_ADDR = 0x0C
AK8963_CNTL1 = 0x0A
AK8963_DATA = 0x03

# === Sensor Initialization ===
def write_byte(addr, reg, data):
    i2c.writeto_mem(addr, reg, bytes([data]))

def read_bytes(addr, reg, n):
    return i2c.readfrom_mem(addr, reg, n)

def mpu_init():
    print("Initializing MPU-9250 in master mode...")
    write_byte(MPU_ADDR, PWR_MGMT_1, 0x00)
    time.sleep_ms(100)

    write_byte(MPU_ADDR, USER_CTRL, 0x20)      # Enable I2C master mode
    write_byte(MPU_ADDR, I2C_MST_CTRL, 0x0D)   # I2C master mode, 400kHz

    # === Step 1: Reset AK8963 using Slave 1 ===
    write_byte(MPU_ADDR, I2C_SLV1_ADDR, AK8963_ADDR)
    write_byte(MPU_ADDR, I2C_SLV1_REG, AK8963_CNTL1)
    write_byte(MPU_ADDR, I2C_SLV1_DO, 0x00)
    write_byte(MPU_ADDR, I2C_SLV1_CTRL, 0x81)
    time.sleep_ms(100)

    # === Step 2: Set AK8963 to continuous mode 2 (100Hz, 16-bit) ===
    write_byte(MPU_ADDR, I2C_SLV1_DO, 0x16)
    write_byte(MPU_ADDR, I2C_SLV1_CTRL, 0x81)
    time.sleep_ms(100)

    # === Step 3: Configure Slave 0 to read 7 bytes from AK8963 ===
    write_byte(MPU_ADDR, I2C_SLV0_ADDR, AK8963_ADDR | 0x80)  # Read mode
    write_byte(MPU_ADDR, I2C_SLV0_REG, AK8963_DATA)
    write_byte(MPU_ADDR, I2C_SLV0_CTRL, 0x87)  # Enable, 7 bytes

    print("MPU-9250 + AK8963 initialization complete.")

def read_accel_gyro_temp():
    raw = read_bytes(MPU_ADDR, ACCEL_XOUT_H, 14)
    data = struct.unpack('>hhhhhhh', raw)
    accel_x, accel_y, accel_z, temp_raw, gyro_x, gyro_y, gyro_z = data
    temp_c = temp_raw / 333.87 + 21
    return (accel_x, accel_y, accel_z), (gyro_x, gyro_y, gyro_z), temp_c

def read_mag():
    data = read_bytes(MPU_ADDR, EXT_SENS_DATA_00, 7)
    if data[0] & 0x01:  # Data ready bit
        return struct.unpack('<hhh', data[1:7])
    return None

# === Main ===
mpu_init()
madgwick = MadgwickAHRS(sample_period=1/100, beta=0.1)

print("pitch,roll,yaw")  # Thonny plotter header

while True:
    try:
        accel, gyro, temp_c = read_accel_gyro_temp()
        ax, ay, az = [v / 16384.0 for v in accel]
        gx, gy, gz = [v / 131.0 for v in gyro]

        mag = read_mag()
        if mag:
            mx, my, mz = mag
            madgwick.update(gx, gy, gz, ax, ay, az, mx, my, mz)
            roll, pitch, yaw = madgwick.get_euler()
            print("{:.2f},{:.2f},{:.2f}".format(pitch, roll, yaw))
        else:
            print("0,0,0")
            print("Q:", madgwick.q)

        # Also print debug info in terminal (optional)
        print("Accel: x={:6d} y={:6d} z={:6d}".format(*accel))
        print("Gyro:  x={:6d} y={:6d} z={:6d}".format(*gyro))
        print("Temp:  {:.2f} °C".format(temp_c))
        print("-" * 40)

        time.sleep(0.5)
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
