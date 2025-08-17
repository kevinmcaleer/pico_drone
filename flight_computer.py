# flight_computer.py
"""
Main flight computer module for the Pico Drone project.
Integrates IMU, Magnetometer, and GPS modules for sensor fusion and control.
"""
try:
      from machine import I2C, UART, Pin
except ImportError:
      from mock_machine import I2C, UART, Pin
import time
import asyncio
from imu_gy91 import IMUGY91
from mag_gy273 import MagnetometerGY273
from gps_neo6m import GPSNEO6M

# Optionally import GamePadServer if available
try:
      from gamepad import GamePadServer
except ImportError:
      GamePadServer = None

# Initialize I2C and UART (adjust pins as needed)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

imu = IMUGY91(i2c)
mag = MagnetometerGY273(i2c)
gps = GPSNEO6M(uart)

def drone_action(gamepad):
      # Replace with actual drone control logic
      if gamepad.is_up:
            print('Drone forward')
      elif gamepad.is_down:
            print('Drone backward')
      elif gamepad.is_left:
            print('Drone left')
      elif gamepad.is_right:
            print('Drone right')
      elif gamepad.is_a:
            print('A button pressed')
      elif gamepad.is_b:
            print('B button pressed')
      elif gamepad.is_x:
            print('X button pressed')
      elif gamepad.is_y:
            print('Y button pressed')
      elif gamepad.is_start:
            print('Start button pressed')
      elif gamepad.is_select:
            print('Select button pressed')
      elif gamepad.is_menu:
            print('Menu button pressed')
      else:
            print('Drone stop/hover')

async def monitor_gamepad(gamepad):
      """
      Monitor the gamepad for commands and act on them.
      """
      while True:
            drone_action(gamepad)
            await asyncio.sleep(0.1)

async def sensor_task():
      """
      Periodically read sensors and print data.
      """
      # Use time.monotonic for cross-platform timing
      last = time.monotonic()
      print("ax,ay,az,gx,gy,gz,tempC,alt_m,pitch,roll,heading,lat,lon,alt_gps")
      while True:
            now = time.monotonic()
            dt = now - last
            last = now

            imu_data = imu.read_all(dt)
            heading = mag.read_heading()
            gps_data = gps.get_location()

            print(f"{imu_data['ax']:.2f},{imu_data['ay']:.2f},{imu_data['az']:.2f},"
                    f"{imu_data['gx']:.2f},{imu_data['gy']:.2f},{imu_data['gz']:.2f},"
                    f"{imu_data['temp']:.2f},{imu_data['alt']:.2f},{imu_data['pitch']:.2f},{imu_data['roll']:.2f},"
                    f"{heading:.2f},{gps_data['lat']:.6f},{gps_data['lon']:.6f},{gps_data['alt']:.2f}")

            await asyncio.sleep(0.1)

async def main():
      if GamePadServer is not None:
            gamepad = GamePadServer()
            blink = asyncio.create_task(gamepad.blink_task())
            monitor = asyncio.create_task(monitor_gamepad(gamepad))
            gamepad.tasks.append(monitor)
            gamepad.tasks.append(blink)
            sensor = asyncio.create_task(sensor_task())
            await asyncio.gather(gamepad.main(), sensor)
      else:
            print("GamePadServer not available, running sensor task only.")
            await sensor_task()

if __name__ == "__main__":
      while True:
            try:
                  asyncio.run(main())
            except KeyboardInterrupt:
                  print("Exiting...")
                  import sys
                  sys.exit()
