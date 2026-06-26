class Battery:
    def __init__(self):
        self.level = 100.0

    def consume(self, amount=0.5):
        self.level -= amount

        if self.level < 0:
            self.level = 0

    def get(self):
        return round(self.level, 1)
