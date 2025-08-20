# gps_test.py
"""
Test script to output live GPS readings (latitude, longitude, altitude) from the NEO-6M module.
"""
from machine import UART, Pin
import time
from gps_neo6m import GPSNEO6M

def main():
    uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
    gps = GPSNEO6M(uart)
    print("Reading GPS data... (Ctrl+C to stop)")
    last_sats = None
    ever_received = False
    while True:
        # Directly check for any raw bytes from UART (RX/TX activity)
        nbytes = uart.any()
        if nbytes:
            ever_received = True
            print(f"[UART RX] {nbytes} bytes available")
            raw_bytes = uart.read(nbytes)
            if raw_bytes:
                try:
                    print(f"[UART RX ASCII] {raw_bytes.decode('ascii', errors='replace')}")
                except Exception as e:
                    print(f"[UART RX RAW] {raw_bytes}")
        elif not ever_received:
            print("[UART RX] No bytes ever received from GPS. Check wiring, power, and pin assignments.")
        sentence = gps.read_sentence()
        if sentence:
            # Parse GPGGA for diagnostics
            parts = sentence.split(',')
            if parts[0] == '$GPGGA':
                try:
                    num_sats = parts[7]
                    if num_sats and num_sats.isdigit():
                        last_sats = int(num_sats)
                    else:
                        last_sats = 0
                    fix_quality = parts[6]
                    if fix_quality and int(fix_quality) > 0:
                        lat = gps._parse_lat(parts[2], parts[3])
                        lon = gps._parse_lon(parts[4], parts[5])
                        hdop = parts[8]
                        alt = parts[9]
                        print(f"Lat: {lat}, Lon: {lon}, Alt: {alt} m | Sats: {last_sats} | Fix: {fix_quality} | HDOP: {hdop}")
                    else:
                        print(f"No fix yet. Satellites in view: {last_sats}")
                except Exception as e:
                    print("Parse error:", e)
        else:
            if last_sats is not None:
                print(f"No new data. Satellites in view: {last_sats}")
            else:
                print("No new data. Waiting for GPS...")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
