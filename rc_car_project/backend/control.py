class CarController:
    def __init__(self):
        self.battery = 100.0
        self.distance = 0.0

    def _move(self):
        if self.battery > 0:
            self.distance += 1.0 # 1m 이동
            self.battery -= 0.5 # 배터리 0.5% 감소

    def forward(self):
        self._move()

    def backward(self):
        self._move()

    def left(self):
        self._move()

    def right(self):
        self._move()

    def get_status(self):
        return {
            "battery": round(self.battery, 1),
            "distance": round(self.distance, 1)
        }