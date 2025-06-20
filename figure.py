import random

from config import cup_w, cup_h, figure_width, colors, figures


class Figure:
    def __init__(self):
        self.shape = random.choice(list(figures.keys()))
        self.rotation = random.randint(0, len(figures[self.shape]) - 1)
        self.field = figures[self.shape][self.rotation] # Ранее map, теперь field

        self.x = int(cup_w / 2) - int(figure_width / 2)
        self.y = -2

        self.going_down = False
        self.going_left = False
        self.going_right = False

        self.color = random.randint(0, len(colors) - 1)

    def __repr__(self):
        figure_map = "\n".join(self.field).replace("x", "@").replace("o", ".")
        return (
            f"FIGURE INFO\n"
            f"shape: {self.shape}\n"
            f"rotation: {self.rotation}\n"
            f"position: {self.x} {self.y}\n"
            f"color: {self.color}\n\n"
            f"{figure_map}"
        )

    def isFigureValid(self):
        return 0 <= self.x < cup_w and self.y < cup_h

    def changeDownState(self, state: bool):
        self.going_down = state

    def changeLeftState(self, state: bool):
        self.going_left = state

    def changeRightState(self, state: bool):
        self.going_right = state