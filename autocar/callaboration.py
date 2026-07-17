# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import time
from pop import Pilot

Car = Pilot.AutoCar()

SPEED = 50
TEST_TIME = 0.75

# 네가 얻은 보정값
test_table = [
    (-1.0, -0.8),
    (-0.8, -0.598),
    (-0.6, -0.457),
    (-0.4, -0.303),
    (-0.2, -0.618),
    (0.0, 0.0),
    (0.2, 0.2),
    (0.4, 0.321),
    (0.6, 0.484),
    (0.8, 0.662),
    (1.0, 0.852),
]

def measure_gyro(steer):
    Car.steering = steer

    Car.forward(SPEED)

    values = []
    start = time.time()

    while time.time() - start < TEST_TIME:
        values.append(float(Car.getGyro("z")))
        time.sleep(0.03)

    Car.stop()
    time.sleep(0.3)

    if len(values) == 0:
        return 0

    return sum(values) / len(values)

print("===== VERIFY =====")

try:
    for desired, corrected in test_table:

        gyro = measure_gyro(corrected)

        print({
            "desired": desired,
            "corrected": corrected,
            "gyro": round(gyro, 1)
        })

        time.sleep(0.5)

finally:
    Car.stop()