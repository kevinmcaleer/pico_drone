from machine import I2C, Pin
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
print("I2C addresses found:", [hex(addr) for addr in i2c.scan()])
