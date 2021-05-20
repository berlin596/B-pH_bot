from adafruit_motorkit import MotorKit
from time import sleep

pump = MotorKit (address = 0x61)

for i in range(5):
    pump.motor1.throttle = 1.0
    sleep(0.83)
    pump.motor1.throttle = 0
    sleep(2)