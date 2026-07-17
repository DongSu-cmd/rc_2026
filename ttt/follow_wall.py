import time
import math
from multiprocessing import Process

from pop.Pilot import get_Control
from pop.LiDAR.rplidar import Rplidar


class LidarExplorer(Process):

    def __init__(self, data_queue, stop_event):
        super().__init__()

        self.data_queue = data_queue
        self.stop_event = stop_event
        self.last_send_time = 0.0

        self.SAFE_FRONT = 600
        self.CRITICAL_FRONT = 350
        self.BACKUP_TARGET = 700
        self.BACKUP_MIN_TIME = 0.5
        self.BACKUP_MAX_TIME = 1.5
        self.backup_start_time = 0.0

        self.TARGET_WALL_DIST = 400
        self.MARGIN = 150

        self.MIN_VALID_DIST = 200
        self.MAX_VALID_DIST = 6000

        self.BASE_SPEED = 50
        self.STEERING_TRIM = 0.0

        self.current_hardware_speed = None
        self.current_hardware_steering = None

        self.robot_pose = {
            "x": 0.0,
            "y": 0.0,
            "theta": math.pi / 2
        }

        self.CMD_TO_METERS_PER_SEC = 0.015
        self.GYRO_SCALE = (1.0 / 131.0) * (math.pi / 180.0)
        self.GYRO_Z_OFFSET = 0.0
        self.GYRO_DIRECTION = 1.0
        self.GYRO_THRESHOLD = 50.0

        self.explore_state = "INIT"

    def calibrate_gyro_offset(self, car):
        print("[GYRO] Calibrating... 차량을 움직이지 마세요.")

        samples = []

        for _ in range(100):
            try:
                samples.append(car.getGyro("z"))
            except Exception as error:
                print("[GYRO] Read error:", error)

            time.sleep(0.03)

        if len(samples) == 0:
            print("[GYRO] Calibration failed.")
            return 0.0

        offset = sum(samples) / len(samples)

        print(f"[GYRO] Offset = {offset:.3f}")

        return offset

    def run(self):
        car = None
        lidar = None

        try:
            car = get_Control()

            self.GYRO_Z_OFFSET = self.calibrate_gyro_offset(car)

            lidar = Rplidar()
            lidar.connect("/dev/ttyUSB0")
            lidar.startMotor()

            print("[LiDAR] Motor started")
            print("[System] Wall-following started")

            last_time = time.time()

            while not self.stop_event.is_set():
                current_time = time.time()
                dt = current_time - last_time
                last_time = current_time

                if dt <= 0.0 or dt > 0.5:
                    dt = 0.05

                try:
                    coords = lidar.getXY()
                except Exception as error:
                    print("[LiDAR] getXY error:", error)
                    time.sleep(0.05)
                    continue

                if coords is None or len(coords) == 0:
                    time.sleep(0.02)
                    continue

                try:
                    lx = coords[:, 0]
                    ly = coords[:, 1]
                except Exception as error:
                    print("[LiDAR] Coordinate error:", error)
                    time.sleep(0.05)
                    continue

                command, target_angle = self.calculate_steering_from_xy(
                    lx,
                    ly,
                    current_time
                )

                self.drive_and_update_pose(
                    car,
                    command,
                    dt
                )

                now = time.time()

                if now - self.last_send_time >= 0.1:
                    status_data = {
                        "x": self.robot_pose["x"],
                        "y": self.robot_pose["y"],
                        "theta": self.robot_pose["theta"],
                        "state": self.explore_state,
                        "command": command,
                        "target_angle": target_angle
                    }

                    self.send_latest_data(status_data)
                    self.last_send_time = now

                time.sleep(0.01)

        except KeyboardInterrupt:
            print("[System] Keyboard interrupt")

        except Exception as error:
            print("[System] Fatal error:", error)

        finally:
            if car is not None:
                try:
                    car.stop()
                    car.steering = 0.0
                except Exception:
                    pass

            if lidar is not None:
                try:
                    lidar.stopMotor()
                except Exception:
                    pass

            print("[System] Vehicle and LiDAR stopped")

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

    def drive_and_update_pose(self, car, command, dt):
        applied_speed = 0.0
        final_steering = self.STEERING_TRIM

        if command == "FORWARD":
            final_steering = self.STEERING_TRIM
            applied_speed = self.BASE_SPEED

        elif command == "TURN_LEFT":
            final_steering = -1.0
            applied_speed = self.BASE_SPEED

        elif command == "BACKWARD":
            final_steering = self.STEERING_TRIM
            applied_speed = -self.BASE_SPEED

        elif command == "SHARP_RIGHT":
            final_steering = 1.0
            applied_speed = self.BASE_SPEED

        elif command == "SMOOTH_RIGHT":
            final_steering = 0.5
            applied_speed = self.BASE_SPEED

        elif command == "FORWARD_RIGHT":
            final_steering = 0.3
            applied_speed = self.BASE_SPEED

        elif command == "FORWARD_LEFT":
            final_steering = -0.3
            applied_speed = self.BASE_SPEED

        elif command == "SHARP_LEFT":
            final_steering = -0.6
            applied_speed = self.BASE_SPEED

        elif command == "STOP":
            final_steering = 0.0
            applied_speed = 0.0

        if final_steering != self.current_hardware_steering:
            car.steering = final_steering
            self.current_hardware_steering = final_steering

        if applied_speed != self.current_hardware_speed:
            if applied_speed > 0:
                car.forward(abs(applied_speed))

            elif applied_speed < 0:
                car.backword(abs(applied_speed))

            else:
                car.stop()

            self.current_hardware_speed = applied_speed

        try:
            raw_gz = car.getGyro("z")
            corrected_gz = raw_gz - self.GYRO_Z_OFFSET
        except Exception:
            corrected_gz = 0.0

        if abs(corrected_gz) > self.GYRO_THRESHOLD:
            angular_velocity = (
                corrected_gz
                * self.GYRO_SCALE
                * self.GYRO_DIRECTION
            )
        else:
            angular_velocity = 0.0

        linear_velocity = (
            applied_speed
            * self.CMD_TO_METERS_PER_SEC
        )

        self.robot_pose["theta"] += angular_velocity * dt

        self.robot_pose["theta"] = math.atan2(
            math.sin(self.robot_pose["theta"]),
            math.cos(self.robot_pose["theta"])
        )

        self.robot_pose["x"] += (
            linear_velocity
            * math.cos(self.robot_pose["theta"])
            * dt
        )

        self.robot_pose["y"] += (
            linear_velocity
            * math.sin(self.robot_pose["theta"])
            * dt
        )

    def calculate_steering_from_xy(self, lx, ly, current_time):
        front_dists = []
        diag_right_dists = []
        right_dists = []

        for raw_x, raw_y in zip(lx, ly):
            x = raw_y
            y = -raw_x

            distance = math.hypot(x, y)

            if distance < self.MIN_VALID_DIST:
                continue

            if distance > self.MAX_VALID_DIST:
                continue

            angle = math.degrees(math.atan2(y, x))

            if x > 0 and abs(y) <= 200:
                front_dists.append(distance)

            if -60 <= angle <= -15:
                diag_right_dists.append(distance)

            if -130 <= angle < -60:
                right_dists.append(distance)

        def get_robust_dist(distance_list, default_value):
            if len(distance_list) < 3:
                return default_value

            return sorted(distance_list)[2]

        front_dist = get_robust_dist(
            front_dists,
            self.MAX_VALID_DIST
        )

        diag_right_dist = get_robust_dist(
            diag_right_dists,
            self.MAX_VALID_DIST
        )

        right_dist = get_robust_dist(
            right_dists,
            self.MAX_VALID_DIST
        )

        if (
            front_dist < self.CRITICAL_FRONT
            and self.explore_state != "BACKING_UP"
        ):
            self.explore_state = "BACKING_UP"
            self.backup_start_time = current_time

        if self.explore_state == "BACKING_UP":
            time_spent = current_time - self.backup_start_time

            backup_finished = (
                time_spent > self.BACKUP_MIN_TIME
                and front_dist >= self.BACKUP_TARGET
            )

            backup_timeout = (
                time_spent > self.BACKUP_MAX_TIME
            )

            if backup_finished or backup_timeout:
                self.explore_state = "ALIGNING"
                return "TURN_LEFT", 90.0

            return "BACKWARD", 0.0

        if self.explore_state == "INIT":
            if front_dist < self.SAFE_FRONT:
                self.explore_state = "ALIGNING"
                return "TURN_LEFT", 90.0

            return "FORWARD", 0.0

        if self.explore_state == "ALIGNING":
            if front_dist < 600:
                return "TURN_LEFT", 90.0

            if right_dist < 1000 or diag_right_dist < 1000:
                self.explore_state = "FOLLOWING"
                return "FORWARD", 0.0

            if (
                front_dist > 1200
                and right_dist > 1200
                and diag_right_dist > 1200
            ):
                self.explore_state = "INIT"
                return "FORWARD", 0.0

            return "TURN_LEFT", 90.0

        if self.explore_state == "FOLLOWING":
            if right_dist > 1000:
                if front_dist < 400:
                    self.explore_state = "ALIGNING"
                    return "TURN_LEFT", 90.0

                return "SHARP_RIGHT", -90.0

            if right_dist > 700:
                if front_dist < 450:
                    self.explore_state = "ALIGNING"
                    return "TURN_LEFT", 90.0

                return "SMOOTH_RIGHT", -45.0

            if front_dist < self.SAFE_FRONT:
                self.explore_state = "ALIGNING"
                return "TURN_LEFT", 90.0

            if right_dist < 180:
                return "SHARP_LEFT", 90.0

            if diag_right_dist < 220:
                return "FORWARD_LEFT", 30.0

            if right_dist > self.TARGET_WALL_DIST + self.MARGIN:
                return "FORWARD_RIGHT", -30.0

            if right_dist < self.TARGET_WALL_DIST - self.MARGIN:
                return "FORWARD_LEFT", 30.0

            return "FORWARD", 0.0

        return "FORWARD", 0.0