from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from backend.control import CarController


class CarApiServer:
    def __init__(self, frontend_dir: Path):
        self.frontend_dir = Path(frontend_dir).resolve()
        self.car = CarController()

        self.app = Flask(
            __name__,
            static_folder=str(self.frontend_dir),
            static_url_path=""
        )

        self.app.add_url_rule("/", "index", self.index)

        self.app.add_url_rule("/api/status",
                              "status",
                              self.status,
                              methods=["GET"])

        self.app.add_url_rule("/api/forward",
                              "forward",
                              self.forward,
                              methods=["POST"])

        self.app.add_url_rule("/api/backward",
                              "backward",
                              self.backward,
                              methods=["POST"])

        self.app.add_url_rule("/api/left",
                              "left",
                              self.left,
                              methods=["POST"])

        self.app.add_url_rule("/api/right",
                              "right",
                              self.right,
                              methods=["POST"])

    def index(self):
        return send_from_directory(self.frontend_dir, "index.html")

    def status(self):
        return jsonify(self.car.get_status())

    def forward(self):
        self.car.forward()
        return jsonify(self.car.get_status())

    def backward(self):
        self.car.backward()
        return jsonify(self.car.get_status())

    def left(self):
        self.car.left()
        return jsonify(self.car.get_status())

    def right(self):
        self.car.right()
        return jsonify(self.car.get_status())

    def run(self):
        self.app.run(host="127.0.0.1", port=5000)