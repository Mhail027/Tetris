class Position:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def flip(self):
        self.x, self.y = self.y, self.x

