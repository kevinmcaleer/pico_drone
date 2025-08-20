# heading_altitude_test.py
"""
Test script to output heading (from magnetometer) and altitude (from IMU barometer), with basic calibration.
"""
from machine import I2C, Pin
import time
from imu_gy91 import IMUGY91
from mag_gy273 import MagnetometerGY273

def calibrate_mag(mag, samples=100):
    print("Calibrating magnetometer... Move the device in all directions.")
    min_x = min_y = min_z = 32767
    max_x = max_y = max_z = -32768
    for _ in range(samples):
        x, y, z = mag.read_raw()
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)
        time.sleep(0.02)
    print("Magnetometer calibration complete.")
    return (min_x, max_x, min_y, max_y, min_z, max_z)

def calibrate_baro(imu, samples=50):
    print("Calibrating barometer... Keep the device still.")
    total = 0
    for _ in range(samples):
        baro = imu.read_bmp280()
        total += baro[1]  # Altitude
        time.sleep(0.05)
    baseline = total / samples
    print(f"Barometer baseline altitude: {baseline:.2f} m")
    return baseline

def main():
    i2c = I2C(0, scl=Pin(1), sda=Pin(0))
    imu = IMUGY91(i2c)
    mag = MagnetometerGY273(i2c)

    # Calibrate sensors
    mag_cal = calibrate_mag(mag)
    baro_base = calibrate_baro(imu)

    print("\nLive heading, altitude, and orientation (Ctrl+C to stop):")
    while True:
        # Magnetometer heading with calibration
        x, y, z = mag.read_raw()
        x_corr = x - (mag_cal[0] + mag_cal[1]) / 2
        y_corr = y - (mag_cal[2] + mag_cal[3]) / 2
        heading = mag.calculate_heading(x_corr, y_corr)
        # Altitude
        _, alt = imu.read_bmp280()
        rel_alt = alt - baro_base
        # Orientation (roll, pitch, yaw)
        try:
            roll, pitch = imu.get_orientation(0.01)
        except Exception:
            roll, pitch = (None, None)
        # Yaw is heading
        print(f"Heading: {heading:.1f}° | Altitude: {rel_alt:+.2f} m | Roll: {roll} | Pitch: {pitch} | Yaw: {heading:.1f}")
        time.sleep(0.05)

if __name__ == "__main__":
    main()
