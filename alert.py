import smbus
import math
import time
import requests

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

bus = smbus.SMBus(1)
address = 0x68  # MPU6050 I2C address

bus.write_byte_data(address, power_mgmt_1, 0)


previous_accel_magnitude = 0
threshold = 0.4  # Adjust this threshold as needed

while True:
    time.sleep(0.1)
    

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0


    accel_magnitude = dist(accel_xout_scaled, accel_yout_scaled)


    if abs(accel_magnitude - previous_accel_magnitude) > threshold:
        print("Earthquake detected!")
        r = requests.post("https://api.pushover.net/1/messages.json", data = {
            "token": "your_token",
            "user": "user",
            "message": "Earthquake Alert"},
            files = {"attachment": ("ek_logo.jpeg", open("ek_logo.jpeg", "rb"), "image/jpeg")})


    previous_accel_magnitude = accel_magnitude

    time.sleep(0.5)
