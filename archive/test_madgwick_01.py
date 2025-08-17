from machine import I2C, Pin
import time
import struct
import math

# === I2C Setup ===
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
MPU_ADDR = 0x68
AK8963_ADDR = 0x0C

# === MPU-9250 and AK8963 Registers ===
PWR_MGMT_1 = 0x6B
INT_PIN_CFG = 0x37
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
AK8963_CNTL1 = 0x0A
AK8963_ST1 = 0x02
AK8963_DATA = 0x03
AK8963_WHO_AM_I = 0x00

# === Madgwick Filter ===
class MadgwickAHRS:
    def __init__(self, beta=0.1):
        self.beta = beta
        self.q = [1, 0, 0, 0]
        self.sample_freq = 100.0

    def update(self, gx, gy, gz, ax, ay, az, mx, my, mz):
        q1, q2, q3, q4 = self.q
        gx *= math.pi / 180
        gy *= math.pi / 180
        gz *= math.pi / 180

        norm = math.sqrt(ax * ax + ay * ay + az * az)
        if norm == 0: return
        ax /= norm
        ay /= norm
        az /= norm

        norm = math.sqrt(mx * mx + my * my + mz * mz)
        if norm == 0: return
        mx /= norm
        my /= norm
        mz /= norm

        # Madgwick algorithm full update omitted for brevity
        # Replace this with full implementation for real use
        # For now, just update a dummy orientation (do nothing)
        self.q = [1, 0, 0, 0]  # Dummy

    def get_euler(self):
        q1, q2, q3, q4 = self.q
        roll = math.atan2(2*(q1*q2 + q3*q4), 1 - 2*(q2*q2 + q3*q3))
        pitch = math.asin(2*(q1*q3 - q4*q2))
        yaw = math.atan2(2*(q1*q4 + q2*q3), 1 - 2*(q3*q3 + q4*q4))
        return (math.degrees(roll), math.degrees(pitch), math.degrees(yaw))

# === Sensor Init ===
def mpu_init():
    print("Waking up MPU-9250...")
    i2c.writeto_mem(MPU_ADDR, PWR_MGMT_1, b'\x00')  # Wake up
    time.sleep_ms(100)

    print("Enabling I2C bypass...")
    i2c.writeto_mem(MPU_ADDR, INT_PIN_CFG, b'\x02')  # BYPASS_EN
    time.sleep_ms(100)

    try:
        ak_id = i2c.readfrom_mem(AK8963_ADDR, AK8963_WHO_AM_I, 1)[0]
    except Exception as e:
        print("AK8963 read error:", e)
        raise

    if ak_id != 0x48:
        raise Exception("AK8963 not detected. WHO_AM_I = 0x{:02X}".format(ak_id))
    else:
        print("AK8963 OK")

    print("Configuring AK8963...")
    i2c.writeto_mem(AK8963_ADDR, AK8963_CNTL1, b'\x16')  # 16-bit, 100Hz
    time.sleep_ms(10)


def read_accel():
    raw = i2c.readfrom_mem(MPU_ADDR, ACCEL_XOUT_H, 6)
    ax, ay, az = struct.unpack('>hhh', raw)
    return (ax, ay, az)

def read_gyro():
    raw = i2c.readfrom_mem(MPU_ADDR, GYRO_XOUT_H, 6)
    gx, gy, gz = struct.unpack('>hhh', raw)
    return (gx, gy, gz)

def read_mag():
    st1 = i2c.readfrom_mem(AK8963_ADDR, AK8963_ST1, 1)[0]
    if not (st1 & 0x01):
        return None
    raw = i2c.readfrom_mem(AK8963_ADDR, AK8963_DATA, 7)
    mx, my, mz = struct.unpack('<hhh', raw[0:6])  # little endian
    return (mx, my, mz)

# === Main ===
mpu_init()
madgwick = MadgwickAHRS()

print("Reading sensors...")

while True:
    try:
        accel = read_accel()
        gyro = read_gyro()
        mag = read_mag()

        if accel and gyro and mag:
            ax, ay, az = [v / 16384.0 for v in accel]  # accel scale ±2g
            gx, gy, gz = [v / 131.0 for v in gyro]     # gyro scale ±250 dps
            mx, my, mz = mag  # magnetometer scale TBD (not scaled here)

            madgwick.update(gx, gy, gz, ax, ay, az, mx, my, mz)
            roll, pitch, yaw = madgwick.get_euler()

            print("Roll: {:.2f}  Pitch: {:.2f}  Yaw: {:.2f}".format(roll, pitch, yaw))
        else:
            print("Waiting for sensor data...")

        time.sleep(0.1)
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
