from machine import Pin, I2C
import time
import math

# === I2C Setup ===
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

# === MPU9250 Registers ===
MPU_ADDR = 0x68
MPU_PWR_MGMT_1 = 0x6B

# === BMP280 Registers ===
BMP_ADDR = 0x76
BMP_TEMP_MSB = 0xFA
BMP_PRESS_MSB = 0xF7
BMP_CTRL_MEAS = 0xF4
BMP_CONFIG = 0xF5

# === Madgwick Filter (No magnetometer) ===
class Madgwick:
    def __init__(self, beta=0.1):
        self.beta = beta
        self.q = [1.0, 0.0, 0.0, 0.0]

    def update(self, gx, gy, gz, ax, ay, az, dt):
        q1, q2, q3, q4 = self.q
        norm = math.sqrt(ax * ax + ay * ay + az * az)
        if norm == 0:
            return
        ax /= norm
        ay /= norm
        az /= norm

        gx = math.radians(gx)
        gy = math.radians(gy)
        gz = math.radians(gz)

        # Quaternion rate of change from gyroscope
        qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz)
        qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy)
        qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx)
        qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx)

        # Integrate to yield quaternion
        q1 += qDot1 * dt
        q2 += qDot2 * dt
        q3 += qDot3 * dt
        q4 += qDot4 * dt

        norm = math.sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4)
        self.q = [q1 / norm, q2 / norm, q3 / norm, q4 / norm]

    def get_euler(self):
        q1, q2, q3, q4 = self.q
        roll = math.atan2(2.0 * (q1 * q2 + q3 * q4), 1.0 - 2.0 * (q2 * q2 + q3 * q3))
        pitch = math.asin(2.0 * (q1 * q3 - q4 * q2))
        return math.degrees(pitch), math.degrees(roll)

# === Sensor Setup ===
# Wake up MPU9250
i2c.writeto_mem(MPU_ADDR, MPU_PWR_MGMT_1, b'\x00')

# BMP280 config
i2c.writeto_mem(BMP_ADDR, BMP_CTRL_MEAS, b'\x27')
i2c.writeto_mem(BMP_ADDR, BMP_CONFIG, b'\xA0')

# === Sensor Reading Functions ===
def read_word(addr, reg):
    data = i2c.readfrom_mem(addr, reg, 2)
    val = data[0] << 8 | data[1]
    return val - 65536 if val > 32767 else val

def read_bmp280():
    data = i2c.readfrom_mem(BMP_ADDR, BMP_TEMP_MSB, 3)
    temp_raw = ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4
    data = i2c.readfrom_mem(BMP_ADDR, BMP_PRESS_MSB, 3)
    press_raw = ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4
    temperature = temp_raw / 5120.0
    pressure = press_raw / 256.0
    return temperature, pressure

def pressure_to_altitude(pressure_pa, sea_level_pa=101325.0):
    return 44330.0 * (1.0 - (pressure_pa / sea_level_pa) ** 0.1903)

# === Madgwick Filter Instance ===
madgwick = Madgwick()

# === Print CSV Header for Thonny Plotter ===
print("ax,ay,az,gx,gy,gz,tempC,alt_m,pitch,roll")

# === Main Loop ===
last = time.ticks_ms()
while True:
    now = time.ticks_ms()
    dt = time.ticks_diff(now, last) / 1000.0
    last = now

    ax = read_word(MPU_ADDR, 0x3B) / 16384.0
    ay = read_word(MPU_ADDR, 0x3D) / 16384.0
    az = read_word(MPU_ADDR, 0x3F) / 16384.0

    gx = read_word(MPU_ADDR, 0x43) / 131.0
    gy = read_word(MPU_ADDR, 0x45) / 131.0
    gz = read_word(MPU_ADDR, 0x47) / 131.0

    temp, press = read_bmp280()
    alt = pressure_to_altitude(press)
    scaled_alt = alt / 100

    madgwick.update(gx, gy, gz, ax, ay, az, dt)
    pitch, roll = madgwick.get_euler()

#     print(f"{ax:.2f},{ay:.2f},{az:.2f},{gx:.2f},{gy:.2f},{gz:.2f},{temp:.2f},{scaled_alt:.2f},{pitch:.2f},{roll:.2f}")
    print(f"{scaled_alt:.2f},{pitch:.2f},{roll:.2f}")

    time.sleep(0.1)
    
