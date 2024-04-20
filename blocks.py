import pygame as pg
from settings import COLORS, CELL_SIZE


class Block:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.is_moving = True

    def collide(self):
        self.is_moving = False

    def fall(self):
        if self.is_moving:
            for point in self.coords:
                point[1] += 1

    def move(self, aside):
        if aside == pg.K_LEFT:
            for point in self.coords:
                point[0] -= 1

        elif aside == pg.K_RIGHT:
            for point in self.coords:
                point[0] += 1

    def rotate(self):
        pass


class Hero_Block(Block):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y
        self.x = x
        self.color = COLORS["Red"]
        self.coords = [
            [self.x, self.y],
            [self.x, self.y + 1],
            [self.x, self.y + 2],
            [self.x, self.y + 3],
        ]


class LL_Block(Block):
    def __init__(self, x, y):
        super().__init__(x)
        self.x = x
        self.y = y
        self.color = COLORS["Yellow"]

        self.coords = [
            [self.x, self.y],
            [self.x, self.y + 1],
            [self.x + 1, self.y + 1],
            [self.x + 2, self.y + 1],
        ]


class LR_Block(Block):
    def __init__(self, x, y):
        super().__init__(x)
        self.x = x
        self.y = y
        self.color = COLORS["Pink"]
        self.coords = [
            [self.x + 2, self.y],
            [self.x, self.y + 1],
            [self.x + 1, self.y + 1],
            [self.x + 2, self.y + 1],
        ]


class ZR_Block(Block):
    def __init__(self, x, y):
        super().__init__(x)
        self.x = x
        self.y = y
        self.color = COLORS["Orange"]
        self.coords = [
            [self.x + 1, self.y],
            [self.x + 2, self.y],
            [self.x, self.y + 1],
            [self.x + 1, self.y + 1],
        ]


class ZL_Block(Block):
    def __init__(self, x, y):
        super().__init__(x)
        self.x = x
        self.y = y
        self.color = COLORS["Cyan"]
        self.coords = [
            [self.x, self.y],
            [self.x + 1, self.y],
            [self.x + 1, self.y + 1],
            [self.x + 2, self.y + 1],
        ]


class T_Block(Block):
    def __init__(self, x, y):
        super().__init__(x)
        self.x = x
        self.y = y
        self.color = COLORS["Blue"]
        self.coords = [
            [self.x + 1, self.y],
            [self.x, self.y + 1],
            [self.x + 1, self.y + 1],
            [self.x + 2, self.y + 1],
        ]


class S_Block(Block):
    def __init__(self, x, y):
        super().__init__(x)
        self.x = x
        self.y = y
        self.color = COLORS["Green"]
        self.coords = [
            [self.x, self.y],
            [self.x + 1, self.y],
            [self.x, self.y + 1],
            [self.x + 1, self.y + 1],
        ]
