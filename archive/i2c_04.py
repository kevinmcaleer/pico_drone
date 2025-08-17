from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
MPU_ADDR = 0x68
AK8963_ADDR = 0x0C

def write_ak8963_reg(reg_addr, value):
    """Write to AK8963 register via MPU9250 I2C_SLV4 interface."""
    # Set slave address (write mode)
    write_mpu(0x31, AK8963_ADDR)  # I2C_SLV4_ADDR
    write_mpu(0x32, reg_addr)     # I2C_SLV4_REG
    write_mpu(0x33, value)        # I2C_SLV4_DO
    write_mpu(0x34, 0x80)         # I2C_SLV4_CTRL (enable write)
    time.sleep_ms(10)


def write_mpu(reg, val):
    i2c.writeto_mem(MPU_ADDR, reg, bytes([val]))

def read_mpu(reg, n=1):
    return i2c.readfrom_mem(MPU_ADDR, reg, n)

def init_mpu9250_master_mode():
    # Wake up MPU-9250
    write_mpu(0x6B, 0x00)       # PWR_MGMT_1 = 0
    time.sleep_ms(100)

    # Disable I2C master first
    write_mpu(0x6A, 0x00)       # USER_CTRL = 0
    time.sleep_ms(10)

    # Enable I2C master mode
    write_mpu(0x6A, 0x20)       # USER_CTRL = I2C_MST_EN
    time.sleep_ms(10)

    # Set I2C master clock
    write_mpu(0x24, 0x0D)       # I2C_MST_CTRL = 400kHz
    time.sleep_ms(10)

    # === WRITE 0x06 to AK8963 register 0x0A using I2C_SLV4 ===
    write_mpu(0x31, 0x0C)       # I2C_SLV4_ADDR = 0x0C
    write_mpu(0x32, 0x0A)       # I2C_SLV4_REG = 0x0A
    write_mpu(0x33, 0x06)       # I2C_SLV4_DO = 0x06 (continuous mode 2)
    write_mpu(0x34, 0x80)       # I2C_SLV4_CTRL = enable write
    time.sleep_ms(10)

    # === Setup I2C_SLV0 to read 7 bytes from AK8963 starting at 0x03 ===
    write_mpu(0x25, 0x8C)       # I2C_SLV0_ADDR = 0x0C (read)
    write_mpu(0x26, 0x03)       # I2C_SLV0_REG = 0x03 (HXL)
    write_mpu(0x27, 0x87)       # I2C_SLV0_CTRL = enable + read 7 bytes
    time.sleep_ms(10)
    
    # === Verify AK8963 CNTL1 register (0x0A) ===
    # Setup I2C_SLV4 to read from AK8963 register 0x0A
    write_mpu(0x31, 0x8C)  # I2C_SLV4_ADDR = 0x0C (read mode)
    write_mpu(0x32, 0x0A)  # I2C_SLV4_REG = 0x0A
    write_mpu(0x34, 0x80)  # I2C_SLV4_CTRL = enable read
    time.sleep_ms(10)

    # Read the result from I2C_SLV4_DI (0x35)
    cntl1 = read_mpu(0x35)[0]
    print("AK8963 CNTL1 register =", hex(cntl1))



def read_magnetometer():
    # EXT_SENS_DATA_00 to 06 → magnetometer data
    raw = read_mpu(0x49, 7)
    x = int.from_bytes(raw[0:2], 'little', True)
    y = int.from_bytes(raw[2:4], 'little', True)
    z = int.from_bytes(raw[4:6], 'little', True)
    return x, y, z

# Run the init
init_mpu9250_master_mode()
# Step 1: Try writing CNTL1 = 0x06 (continuous mode)
write_ak8963_reg(0x0A, 0x06)

# Step 2: Confirm by reading it back (up to 5 tries)
for i in range(5):
    # Set up I2C_SLV4 read
    write_mpu(0x31, 0x8C)      # Read mode
    write_mpu(0x32, 0x0A)      # Register = CNTL1
    write_mpu(0x34, 0x80)      # Enable read
    time.sleep_ms(10)
    cntl1 = read_mpu(0x35)[0]
    print(f"Try {i+1}: CNTL1 =", hex(cntl1))
    if cntl1 == 0x06:
        print("✅ AK8963 is in continuous mode.")
        break
    time.sleep_ms(50)
else:
    print("❌ Failed to write AK8963 CNTL1. Magnetometer will not work.")

# Read loop
print("Reading magnetometer via internal I2C master...")
while True:
    try:
        mag = read_magnetometer()
        print("Magnetometer (raw):", mag)
        time.sleep(0.5)
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
