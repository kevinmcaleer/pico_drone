from machine import UART, Pin
import time

# Setup UART1 (TX on GP4, RX on GP5 for Pico)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

def parse_lat_long(raw_lat, raw_dir, raw_lon, lon_dir):
    # Convert raw NMEA format to decimal degrees
    try:
        lat_deg = int(raw_lat[:2])
        lat_min = float(raw_lat[2:])
        latitude = lat_deg + (lat_min / 60.0)
        if raw_dir == 'S':
            latitude *= -1

        lon_deg = int(raw_lon[:3])
        lon_min = float(raw_lon[3:])
        longitude = lon_deg + (lon_min / 60.0)
        if lon_dir == 'W':
            longitude *= -1

        return latitude, longitude
    except:
        return None, None

def read_gps():
    while True:
        if uart.any():
            line = uart.readline()
            if not line:
                continue
            try:
                line = line.decode('utf-8').strip()
#                 print(f"line: {line}")
                if line.startswith('$GPRMC'):
                    parts = line.split(',')
                    if parts[2] == 'A':  # Valid data
                        lat, lon = parse_lat_long(parts[3], parts[4], parts[5], parts[6])
                        print("Time (UTC):", parts[1])
                        print("Latitude:", lat)
                        print("Longitude:", lon)
                        print("Speed (knots):", parts[7])
                        print("Date (DDMMYY):", parts[9])
                        print("-" * 40)
                    else:
                        print("No GPS fix yet.")
                elif line.startswith('$GPGGA'):
                    parts = line.split(',')
                    if len(parts) >= 11:
                        print("Fix Quality:", parts[6])
                        print("Satellites in use:", parts[7])
                        print("Altitude:", parts[9], parts[10])
                    else:
                        print("Incomplete GPGGA sentence:", parts)
                elif line.startswith('$GPGSV'):
                    print("Satellites info:", line)
            except Exception as e:
                print("Decode error:", e)
        time.sleep(0.1)

# Run the GPS reader
print("Waiting for GPS data...")
read_gps()
