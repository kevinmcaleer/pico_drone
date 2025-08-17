# imu_gy91.py
"""
Module for interfacing with the GY-91 IMU sensor (accelerometer, gyroscope, barometer) on the Raspberry Pi Pico 2W using MicroPython.
"""
from machine import I2C
import math

MPU_ADDR = 0x68
MPU_PWR_MGMT_1 = 0x6B
BMP_ADDR = 0x76
BMP_TEMP_MSB = 0xFA
BMP_PRESS_MSB = 0xF7
BMP_CTRL_MEAS = 0xF4
BMP_CONFIG = 0xF5

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
        qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz)
        qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy)
        qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx)
        qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx)
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

class IMUGY91:
    def __init__(self, i2c):
        self.i2c = i2c
        self.madgwick = Madgwick()
        self._init_sensors()

    def _init_sensors(self):
        self.i2c.writeto_mem(MPU_ADDR, MPU_PWR_MGMT_1, b'\x00')
        self.i2c.writeto_mem(BMP_ADDR, BMP_CTRL_MEAS, b'\x27')
        self.i2c.writeto_mem(BMP_ADDR, BMP_CONFIG, b'\xA0')

    def read_word(self, addr, reg):
        data = self.i2c.readfrom_mem(addr, reg, 2)
        val = data[0] << 8 | data[1]
        return val - 65536 if val > 32767 else val

    def read_accel(self):
        ax = self.read_word(MPU_ADDR, 0x3B) / 16384.0
        ay = self.read_word(MPU_ADDR, 0x3D) / 16384.0
        az = self.read_word(MPU_ADDR, 0x3F) / 16384.0
        return ax, ay, az

    def read_gyro(self):
        gx = self.read_word(MPU_ADDR, 0x43) / 131.0
        gy = self.read_word(MPU_ADDR, 0x45) / 131.0
        gz = self.read_word(MPU_ADDR, 0x47) / 131.0
        return gx, gy, gz

    def read_bmp280(self):
        data = self.i2c.readfrom_mem(BMP_ADDR, BMP_TEMP_MSB, 3)
        temp_raw = ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4
        data = self.i2c.readfrom_mem(BMP_ADDR, BMP_PRESS_MSB, 3)
        press_raw = ((data[0] << 16) | (data[1] << 8) | data[2]) >> 4
        temperature = temp_raw / 5120.0
        pressure = press_raw / 256.0
        return temperature, pressure

    def pressure_to_altitude(self, pressure_pa, sea_level_pa=101325.0):
        return 44330.0 * (1.0 - (pressure_pa / sea_level_pa) ** 0.1903)

    def get_orientation(self, dt):
        ax, ay, az = self.read_accel()
        gx, gy, gz = self.read_gyro()
        self.madgwick.update(gx, gy, gz, ax, ay, az, dt)
        return self.madgwick.get_euler()

    def read_all(self, dt):
        ax, ay, az = self.read_accel()
        gx, gy, gz = self.read_gyro()
        temp, press = self.read_bmp280()
        alt = self.pressure_to_altitude(press)
        pitch, roll = self.get_orientation(dt)
        return {
            'ax': ax, 'ay': ay, 'az': az,
            'gx': gx, 'gy': gy, 'gz': gz,
            'temp': temp, 'press': press, 'alt': alt,
            'pitch': pitch, 'roll': roll
        }
