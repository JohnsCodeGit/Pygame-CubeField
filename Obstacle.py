import random

class Obstacle:
    size = .1
    x_pos = 0
    y_pos = 0
    ID = 0
    color = (255, 255, 255)
    def __init__(self, WIDTH):
        self.size = 1
        self.x_pos = random.randint(0, WIDTH-25)
        self.y_pos = random.randint(-800, -100)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

