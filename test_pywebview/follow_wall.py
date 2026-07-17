import time
import math
import numpy as np
from multiprocessing import Process

from pop.LiDAR.rplidar import Rplidar
from pop.Pilot import get_Control


class LidarExplorer(Process):

    def __init__(self, data_queue, stop_event, run_event):
        super().__init__()

        self.data_queue = data_queue
        self.stop_event = stop_event
        self.run_event = run_event

        self.MIN_DISTANCE = 200
        self.MAX_DISTANCE = 3000
        self.SEND_INTERVAL = 0.1

        self.last_send_time = 0.0
        self.theta = 0.0

        self.GYRO_SCALE = (
            1.0 / 131.0
        ) * (
            math.pi / 180.0
        )

        self.GYRO_OFFSET = 0.0

    def run(self):

        car = get_Control()

        samples = []

        for _ in range(100):

            samples.append(
                car.getGyro("z")
            )

            time.sleep(0.02)

        self.GYRO_OFFSET = (
            sum(samples)
            /
            len(samples)
        )

        print(
            "gyro offset =",
            self.GYRO_OFFSET
        )

        lidar = Rplidar()
        try:
            print("[LiDAR] Connecting to /dev/ttyUSB0")

            lidar.connect("/dev/ttyUSB0")
            lidar.startMotor()

            print("[LiDAR] Motor started")
            print("[LiDAR] Waiting for start button")
            last_time = time.time()

            while not self.stop_event.is_set():
                current_time = time.time()

                dt = current_time - last_time

                last_time = current_time
                if not self.run_event.is_set():
                    time.sleep(0.1)
                    continue

                try:
                    coords = lidar.getXY()
                except Exception as error:
                    print("[LiDAR] getXY error:", error)
                    time.sleep(0.1)
                    continue

                if coords is None or len(coords) == 0:
                    time.sleep(0.05)
                    continue
                gz = (
                    car.getGyro("z")
                    - self.GYRO_OFFSET
                )

                if abs(gz) > 50:

                    self.theta += (
                        gz
                        * self.GYRO_SCALE
                        * dt
                    )
                coords = np.asarray(coords)

                if coords.ndim != 2 or coords.shape[1] < 2:
                    print("[LiDAR] Invalid coordinate shape:", coords.shape)
                    time.sleep(0.05)
                    continue

                local_scan = np.column_stack((
                    coords[:, 0],
                    coords[:, 1]
                ))

                filtered_scan = []
                distances = []

                for point in local_scan:
                    x = float(point[0])
                    y = float(point[1])
                    distance = math.hypot(x, y)

                    if distance < self.MIN_DISTANCE:
                        continue

                    if distance > self.MAX_DISTANCE:
                        continue

                    filtered_scan.append([x, y])
                    distances.append(distance)

                if len(distances) > 0:
                    min_distance = min(distances)
                    max_distance = max(distances)
                else:
                    min_distance = 0.0
                    max_distance = 0.0

                now = time.time()

                if now - self.last_send_time >= self.SEND_INTERVAL:
                    status_data = {
                        "scan": filtered_scan,
                        "theta": self.theta,
                        "point_count": len(filtered_scan),
                        "min_distance": min_distance,
                        "max_distance": max_distance,
                        "running": True,
                        "coordinate_type": "local_mm"
                    }

                    self.send_latest_data(status_data)

                    print(
                        f"[LiDAR] points={len(filtered_scan)} "
                        f"min={min_distance:.0f}mm "
                        f"max={max_distance:.0f}mm"
                    )

                    self.last_send_time = now

                time.sleep(0.02)

        except Exception as error:
            print("[LiDAR] Fatal error:", error)

            self.send_latest_data({
                "scan": [],
                "point_count": 0,
                "min_distance": 0.0,
                "max_distance": 0.0,
                "running": False,
                "error": str(error),
                "coordinate_type": "local_mm"
            })

        finally:
            try:
                lidar.stopMotor()
            except Exception:
                pass

            print("[LiDAR] Motor stopped")

    def send_latest_data(self, status_data):
        try:
            while not self.data_queue.empty():
                self.data_queue.get_nowait()
        except Exception:
            pass

        try:
            self.data_queue.put_nowait(status_data)
        except Exception:
            pass