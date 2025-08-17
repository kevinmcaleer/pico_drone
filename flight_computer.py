# flight_computer.py
"""
Main flight computer module for the Pico Drone project.
Integrates IMU, Magnetometer, and GPS modules for sensor fusion and control.
"""
from machine import I2C, UART, Pin
import time
from imu_gy91 import IMUGY91
from mag_gy273 import MagnetometerGY273
from gps_neo6m import GPSNEO6M

# Initialize I2C and UART (adjust pins as needed)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

imu = IMUGY91(i2c)
mag = MagnetometerGY273(i2c)
gps = GPSNEO6M(uart)

last = time.ticks_ms()

print("ax,ay,az,gx,gy,gz,tempC,alt_m,pitch,roll,heading,lat,lon,alt_gps")

while True:
    now = time.ticks_ms()
    dt = time.ticks_diff(now, last) / 1000.0
    last = now

    imu_data = imu.read_all(dt)
    heading = mag.read_heading()
    gps_data = gps.get_location()

    print(f"{imu_data['ax']:.2f},{imu_data['ay']:.2f},{imu_data['az']:.2f},"
          f"{imu_data['gx']:.2f},{imu_data['gy']:.2f},{imu_data['gz']:.2f},"
          f"{imu_data['temp']:.2f},{imu_data['alt']:.2f},{imu_data['pitch']:.2f},{imu_data['roll']:.2f},"
          f"{heading:.2f},{gps_data['lat']:.6f},{gps_data['lon']:.6f},{gps_data['alt']:.2f}")

    time.sleep(0.1)
