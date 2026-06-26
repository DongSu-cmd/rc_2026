class Distance:
    def __init__(self):
        self.distance = 0.0

    def move(self, value=1.0):
        self.distance += value

    def get(self):
        return round(self.distance, 1)