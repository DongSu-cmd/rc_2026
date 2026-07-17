import time
import math
import threading
import numpy as np

from flask import Flask, jsonify, render_template_string

from pop.Pilot import get_Control
from pop.LiDAR.rplidar import Rplidar

app = Flask(__name__)

latest_data = {
    "x": 0.0,
    "y": 0.0,
    "theta": 0.0,
    "scan": []
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>IMU Mapping Test</title>
<style>
body{
    background:#000;
    color:white;
    margin:0;
}
canvas{
    display:block;
    margin:auto;
    background:#001018;
}
</style>
</head>
<body>

<canvas id="map" width="1200" height="800"></canvas>

<script>

const canvas =
document.getElementById("map");

const ctx =
canvas.getContext("2d");

let mapPoints =
new Map();

async function update(){

    const res =
    await fetch("/api/status");

    const data =
    await res.json();

    draw(data);
}

function draw(data){

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    for(const p of data.scan){

        const worldX =
            p[0] +
            data.x;

        const worldY =
            p[1] +
            data.y;

        const gx =
            Math.round(worldX / 30);

        const gy =
            Math.round(worldY / 30);

        mapPoints.set(
            gx + "," + gy,
            {
                x : gx * 30,
                y : gy * 30
            }
        );
    }

    ctx.fillStyle = "lime";

    for(const p of mapPoints.values()){

        ctx.fillRect(
            600 + p.x / 10,
            400 - p.y / 10,
            2,
            2
        );
    }

    ctx.fillStyle = "red";

    ctx.beginPath();

    ctx.arc(
        600 + latestRobotX,
        400 - latestRobotY,
        8,
        0,
        Math.PI * 2
    );

    ctx.fill();
}

let latestRobotX = 0;
let latestRobotY = 0;

setInterval(async()=>{

    const res =
    await fetch("/api/status");

    const data =
    await res.json();

    latestRobotX =
        data.x / 10;

    latestRobotY =
        data.y / 10;

    draw(data);

},100);

</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/status")
def status():
    return jsonify(latest_data)


def mapping_thread():

    car = get_Control()

    lidar = Rplidar()

    lidar.connect("/dev/ttyUSB0")

    lidar.startMotor()

    print("Gyro Calibration")

    gyro_samples = []

    for _ in range(100):

        gyro_samples.append(
            car.getGyro("z")
        )

        time.sleep(0.02)

    gyro_offset = (
        sum(gyro_samples)
        /
        len(gyro_samples)
    )

    print(
        "gyro_offset =",
        gyro_offset
    )

    theta = 0.0

    x = 0.0
    y = 0.0

    vx = 0.0
    vy = 0.0

    last_time = time.time()

    car.forward(50)

    move_start = time.time()

    try:

        while True:

            now = time.time()

            dt = now - last_time

            last_time = now

            if now - move_start > 5:

                car.stop()

            try:

                coords =
                    lidar.getXY()

                if coords is None:
                    continue

                scan_coords = np.column_stack((
                    coords[:,1],
                    -coords[:,0]
                ))

            except Exception:

                continue

            ax =
                car.getAccel("x")

            ay =
                car.getAccel("y")

            gz =
                car.getGyro("z")

            if abs(ax) < 0.05:
                ax = 0.0

            if abs(ay) < 0.05:
                ay = 0.0

            vx += ax * dt
            vy += ay * dt

            move_mag = math.hypot(
                vx,
                vy
            )

            if move_mag > 0.001:

                x += vx * dt * 500
                y += vy * dt * 500

            corrected_gz =
                gz - gyro_offset

            if abs(corrected_gz) > 50:

                theta += (
                    corrected_gz
                    *
                    (1.0/131.0)
                    *
                    math.pi/180.0
                    *
                    dt
                )

            filtered = []

            for p in scan_coords:

                dist =
                    math.hypot(
                        p[0],
                        p[1]
                    )

                if dist < 2000:

                    filtered.append(
                        p.tolist()
                    )

            latest_data["x"] = x
            latest_data["y"] = y
            latest_data["theta"] = theta
            latest_data["scan"] = filtered[::4]

            print(
                f"x={x:.1f} "
                f"y={y:.1f} "
                f"theta={math.degrees(theta):.1f}"
            )

            time.sleep(0.05)

    finally:

        try:
            car.stop()
        except:
            pass

        try:
            lidar.stopMotor()
        except:
            pass


threading.Thread(
    target=mapping_thread,
    daemon=True
).start()

app.run(
    host="0.0.0.0",
    port=5000,
    debug=False
)