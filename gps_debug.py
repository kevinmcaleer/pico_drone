from machine import UART
import time

uart = UART(1, baudrate=9600, tx=4, rx=5)

while True:
    if uart.any():
        data = uart.readline()
        if data:
            print(data)
    time.sleep(0.1)
