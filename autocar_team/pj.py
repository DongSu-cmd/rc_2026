import csv
import json
import math
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock, Thread
from urllib.parse import parse_qs, urlparse

try:
    import webview
except ImportError:
    webview = None

from pop import Cds, Pilot, delay


HOST = "0.0.0.0"
PORT = 8050
CSV_PATH = "autocar_log.csv"


HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AutoCar Dashboard</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f2f4f7;
      color: #1f2933;
    }
    header {
      background: #1f2933;
      color: white;
      padding: 14px 18px;
      font-size: 20px;
      font-weight: 700;
    }
    main {
      padding: 16px;
      display: grid;
      grid-template-columns: 330px 1fr;
      gap: 16px;
    }
    section {
      background: white;
      border: 1px solid #d8dee6;
      border-radius: 6px;
      padding: 14px;
    }
    h2 {
      margin: 0 0 12px;
      font-size: 16px;
    }
    button {
      height: 36px;
      margin: 3px;
      padding: 0 12px;
      border: 1px solid #b8c2cc;
      border-radius: 5px;
      background: #ffffff;
      cursor: pointer;
    }
    button.primary {
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }
    button.danger {
      background: #dc2626;
      color: white;
      border-color: #dc2626;
    }
    label {
      display: block;
      margin: 12px 0 4px;
      font-size: 13px;
      color: #52606d;
    }
    input[type="range"] {
      width: 100%;
    }
    .value {
      font-weight: 700;
      color: #102a43;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }
    canvas {
      width: 100%;
      height: 360px;
      border: 1px solid #d8dee6;
      border-radius: 4px;
      background: #ffffff;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    td {
      padding: 5px 0;
      border-bottom: 1px solid #edf1f5;
    }
    td:last-child {
      text-align: right;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <header>AutoCar Dashboard</header>
  <main>
    <section>
      <h2>Control</h2>
      <button class="primary" onclick="sendCommand('start')">Start</button>
      <button class="danger" onclick="sendCommand('stop')">Stop</button>
      <button onclick="sendCommand('zero')">Zero</button>
      <button onclick="sendCommand('save')">Save CSV</button>

      <label>Speed: <span id="speedValue" class="value">0</span></label>
      <input id="speed" type="range" min="-99" max="99" step="1" value="0" oninput="setControl()">

      <label>Steering: <span id="steeringValue" class="value">0</span></label>
      <input id="steering" type="range" min="-1" max="1" step="0.05" value="0" oninput="setControl()">

      <h2 style="margin-top:18px;">Status</h2>
      <table>
        <tr><td>Running</td><td id="running">false</td></tr>
        <tr><td>Gyro X</td><td id="gyroX">0</td></tr>
        <tr><td>Gyro Y</td><td id="gyroY">0</td></tr>
        <tr><td>Gyro Z</td><td id="gyroZ">0</td></tr>
        <tr><td>CDS</td><td id="cds">0</td></tr>
        <tr><td>Position X</td><td id="posX">0</td></tr>
        <tr><td>Position Y</td><td id="posY">0</td></tr>
        <tr><td>Distance</td><td id="distance">0</td></tr>
        <tr><td>Motor Angle</td><td id="motorAngle">0</td></tr>
        <tr><td>CSV</td><td id="csv">autocar_log.csv</td></tr>
      </table>
    </section>

    <div class="grid">
      <section>
        <h2>CDS Scatter</h2>
        <canvas id="cdsCanvas" width="760" height="360"></canvas>
      </section>
      <section>
        <h2>Current Position Map</h2>
        <canvas id="mapCanvas" width="760" height="360"></canvas>
      </section>
    </div>
  </main>

  <script>
    let rows = [];

    function sendCommand(command) {
      fetch('/command?name=' + command).then(update);
    }

    function setControl() {
      const speed = document.getElementById('speed').value;
      const steering = document.getElementById('steering').value;
      document.getElementById('speedValue').textContent = speed;
      document.getElementById('steeringValue').textContent = steering;
      fetch('/control?speed=' + speed + '&steering=' + steering);
    }

    function fmt(value, digits) {
      const n = Number(value);
      if (!Number.isFinite(n)) return '0';
      return n.toFixed(digits);
    }

    function drawScatter(canvasId, xKey, yKey, color) {
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = '#d8dee6';
      ctx.strokeRect(40, 20, canvas.width - 60, canvas.height - 60);

      if (rows.length < 1) return;

      const xs = rows.map(r => Number(r[xKey]));
      const ys = rows.map(r => Number(r[yKey]));
      const minX = Math.min(...xs);
      const maxX = Math.max(...xs);
      const minY = Math.min(...ys);
      const maxY = Math.max(...ys);
      const spanX = Math.max(maxX - minX, 1);
      const spanY = Math.max(maxY - minY, 1);

      ctx.fillStyle = color;
      for (const row of rows) {
        const x = 40 + ((Number(row[xKey]) - minX) / spanX) * (canvas.width - 60);
        const y = 20 + (1 - ((Number(row[yKey]) - minY) / spanY)) * (canvas.height - 60);
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    function drawMap() {
      const canvas = document.getElementById('mapCanvas');
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = '#d8dee6';
      ctx.strokeRect(40, 20, canvas.width - 60, canvas.height - 60);

      if (rows.length < 1) return;

      const xs = rows.map(r => Number(r.position_x));
      const ys = rows.map(r => Number(r.position_y));
      const minX = Math.min(...xs);
      const maxX = Math.max(...xs);
      const minY = Math.min(...ys);
      const maxY = Math.max(...ys);
      const spanX = Math.max(maxX - minX, 0.1);
      const spanY = Math.max(maxY - minY, 0.1);

      ctx.strokeStyle = '#2563eb';
      ctx.lineWidth = 2;
      ctx.beginPath();
      rows.forEach((row, i) => {
        const x = 40 + ((Number(row.position_x) - minX) / spanX) * (canvas.width - 60);
        const y = 20 + (1 - ((Number(row.position_y) - minY) / spanY)) * (canvas.height - 60);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();

      const last = rows[rows.length - 1];
      const x = 40 + ((Number(last.position_x) - minX) / spanX) * (canvas.width - 60);
      const y = 20 + (1 - ((Number(last.position_y) - minY) / spanY)) * (canvas.height - 60);
      ctx.fillStyle = '#dc2626';
      ctx.beginPath();
      ctx.arc(x, y, 7, 0, Math.PI * 2);
      ctx.fill();
    }

    function render(data) {
      const latest = data.latest || {};
      rows = data.rows || [];
      document.getElementById('running').textContent = data.running;
      document.getElementById('gyroX').textContent = fmt(latest.gyro_x, 2);
      document.getElementById('gyroY').textContent = fmt(latest.gyro_y, 2);
      document.getElementById('gyroZ').textContent = fmt(latest.gyro_z, 2);
      document.getElementById('cds').textContent = latest.cds || 0;
      document.getElementById('posX').textContent = fmt(latest.position_x, 3);
      document.getElementById('posY').textContent = fmt(latest.position_y, 3);
      document.getElementById('distance').textContent = fmt(latest.distance_m, 3) + ' m';
      document.getElementById('motorAngle').textContent = fmt(latest.motor_angle_deg, 2) + ' deg';
      document.getElementById('csv').textContent = data.csv_path;
      drawScatter('cdsCanvas', 'elapsed', 'cds', '#16a34a');
      drawMap();
    }

    function update() {
      fetch('/data').then(r => r.json()).then(render);
    }

    setControl();
    update();
    setInterval(update, 500);
  </script>
</body>
</html>
"""


class AutoCarWebDashboard:
    def __init__(self, sample_ms=100, csv_path=CSV_PATH):
        self.car = Pilot.AutoCar()
        self.cds = Cds(7)
        self.sample_ms = sample_ms
        self.csv_path = csv_path
        self.lock = Lock()

        self.zero = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.position = {"x": 0.0, "y": 0.0}
        self.heading_deg = 0.0
        self.distance_m = 0.0
        self.motor_angle_deg = 0.0
        self.speed = 0.0
        self.steering = 0.0
        self.running = False
        self.rows = []
        self.start_time = time.time()
        self.last_time = time.time()

        self.speed_to_mps = 0.01
        self.wheel_diameter_m = 0.065
        self.steering_gain = 30.0

    def read_gyro(self):
        value = self.car.getGyro()
        if isinstance(value, dict):
            return {
                "x": float(value.get("x", 0)),
                "y": float(value.get("y", 0)),
                "z": float(value.get("z", 0)),
            }
        return {"x": 0.0, "y": 0.0, "z": 0.0}

    def zero_gyro(self):
        with self.lock:
            self.zero = self.read_gyro()
            self.position = {"x": 0.0, "y": 0.0}
            self.heading_deg = 0.0
            self.distance_m = 0.0
            self.motor_angle_deg = 0.0
            self.rows = []
            self.start_time = time.time()
            self.last_time = self.start_time

    def set_control(self, speed=None, steering=None):
        with self.lock:
            if speed is not None:
                self.speed = max(-99.0, min(99.0, float(speed)))
            if steering is not None:
                self.steering = max(-1.0, min(1.0, float(steering)))

    def start(self):
        self.zero_gyro()
        self.running = True

    def stop(self):
        self.running = False
        self.car.stop()
        self.save_csv()

    def apply_motor(self):
        self.car.steering = self.steering
        if self.speed > 0:
            self.car.forward(abs(self.speed))
        elif self.speed < 0:
            self.car.backward(abs(self.speed))
        else:
            self.car.stop()

    def update_position(self, dt):
        speed_mps = self.speed * self.speed_to_mps
        move_m = speed_mps * dt
        self.heading_deg += self.steering * self.steering_gain * dt
        heading_rad = math.radians(self.heading_deg)

        self.position["x"] += move_m * math.cos(heading_rad)
        self.position["y"] += move_m * math.sin(heading_rad)
        self.distance_m += abs(move_m)

        wheel_round_m = math.pi * self.wheel_diameter_m
        if wheel_round_m > 0:
            self.motor_angle_deg += (move_m / wheel_round_m) * 360

    def collect_once(self):
        now = time.time()
        dt = now - self.last_time
        elapsed = now - self.start_time
        self.last_time = now

        self.apply_motor()
        gyro = self.read_gyro()
        zeroed = {
            "x": gyro["x"] - self.zero["x"],
            "y": gyro["y"] - self.zero["y"],
            "z": gyro["z"] - self.zero["z"],
        }
        cds_value = self.cds.read()
        self.update_position(dt)

        row = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed": round(elapsed, 3),
            "gyro_x": zeroed["x"],
            "gyro_y": zeroed["y"],
            "gyro_z": zeroed["z"],
            "cds": cds_value,
            "speed": self.speed,
            "steering": self.steering,
            "motor_angle_deg": self.motor_angle_deg,
            "distance_m": self.distance_m,
            "position_x": self.position["x"],
            "position_y": self.position["y"],
            "heading_deg": self.heading_deg,
        }
        self.rows.append(row)

    def loop(self):
        while True:
            if self.running:
                with self.lock:
                    self.collect_once()
                    if len(self.rows) % 10 == 0:
                        self.save_csv()
            delay(self.sample_ms)

    def save_csv(self):
        if not self.rows:
            return
        with open(self.csv_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(self.rows[0].keys()))
            writer.writeheader()
            writer.writerows(self.rows)

    def data(self):
        with self.lock:
            return {
                "running": self.running,
                "csv_path": self.csv_path,
                "latest": self.rows[-1] if self.rows else {},
                "rows": self.rows[-300:],
            }


dashboard = AutoCarWebDashboard()


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, _format, *args):
        return

    def send_text(self, text, content_type="text/html"):
        data = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.send_text(HTML)
            return

        if parsed.path == "/data":
            self.send_text(json.dumps(dashboard.data()), "application/json")
            return

        if parsed.path == "/control":
            query = parse_qs(parsed.query)
            speed = query.get("speed", [None])[0]
            steering = query.get("steering", [None])[0]
            dashboard.set_control(speed=speed, steering=steering)
            self.send_text("ok", "text/plain")
            return

        if parsed.path == "/command":
            query = parse_qs(parsed.query)
            name = query.get("name", [""])[0]
            if name == "start":
                dashboard.start()
            elif name == "stop":
                dashboard.stop()
            elif name == "zero":
                dashboard.zero_gyro()
            elif name == "save":
                dashboard.save_csv()
            self.send_text("ok", "text/plain")
            return

        self.send_response(404)
        self.end_headers()


def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def main():
    worker = Thread(target=dashboard.loop)
    worker.daemon = True
    worker.start()

    ip = get_ip_address()
    url = "http://{}:{}".format(ip, PORT)
    print("AutoCar web dashboard:", url)
    print("Stop server: Ctrl+C")

    server = HTTPServer((HOST, PORT), DashboardHandler)

    if webview is not None and os.environ.get("DISPLAY"):
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        webview.create_window("AutoCar Dashboard", url)
        webview.start()
        dashboard.stop()
        server.server_close()
        return

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        dashboard.stop()
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
