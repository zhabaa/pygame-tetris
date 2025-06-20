# figure.py
import random
from config import figures, colors

class Figure:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = random.randint(0, len(figures[shape]) - 1)
        self.color = random.randint(0, len(colors) - 1)

    def get_shape_matrix(self):
        return figures[self.shape][self.rotation]