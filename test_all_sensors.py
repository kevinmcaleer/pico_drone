# test_all_sensors.py
"""
Minimal script to test each sensor/module on the Pico individually.
Comment/uncomment blocks as needed for your hardware.
"""
from time import sleep


# --- Rolling Sensor Test Loop ---
try:
    from imu_gy91 import IMUGY91
    from mag_gy273 import MagnetometerGY273
    from gps_neo6m import GPSNEO6M
    from drv8833 import DRV8833
    from machine import I2C, Pin, UART
    import time

    i2c = I2C(0, scl=Pin(1), sda=Pin(0))
    imu = IMUGY91(i2c)
    mag = MagnetometerGY273(i2c)
#     uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
    uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
    gps = GPSNEO6M(uart)


    print("Starting rolling sensor test. Press Ctrl+C to stop.")
    while True:
        # IMU
        try:
            accel = imu.read_accel()
            gyro = imu.read_gyro()
            baro = imu.read_bmp280()
            orient = imu.get_orientation(0.01)
            print("IMU Accel:", accel)
            print("IMU Gyro:", gyro)
            print("IMU Baro:", baro)
            print("IMU Orientation:", orient)
        except Exception as e:
            print("IMU error:", e)

        # Magnetometer
        try:
            x, y, z = mag.read_raw()
            heading = mag.calculate_heading(x, y)
            print("Magnetometer (QMC5883L) raw:", x, y, z)
            print("Magnetometer heading:", heading)
        except Exception as e:
            print("Magnetometer error:", e)

        # GPS (prints first valid sentence/parsed data)
        try:
            sentence = gps.read_sentence()
            if sentence:
                print("GPS sentence:", sentence)
                data = gps.parse_gpgga(sentence)
                if data:
                    print("GPS parsed:", data)
        except Exception as e:
            print("GPS error:", e)



        print("-" * 40)
        time.sleep(1)
except KeyboardInterrupt:
    print("Rolling sensor test stopped.")
except Exception as e:
    print("Fatal error in rolling test:", e)
