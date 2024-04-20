import pygame as pg
from settings import COLORS, CELL_SIZE, DEFAULT_LEFT, DEFAULT_TOP


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = DEFAULT_LEFT
        self.top = DEFAULT_TOP
        self.cell_size = CELL_SIZE

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pg.draw.rect(
                    surface=screen,
                    color=COLORS['White'],
                    rect=(
                        x * self.cell_size + self.left,
                        y * self.cell_size + self.top,
                        self.cell_size,
                        self.cell_size,
                    ),
                    width=1,
                )

    def draw_blocks(self, screen, blocks):
        for block in blocks:
            color = block.color

            for block_chunk in block.coords:
                x, y = block_chunk

                pg.draw.rect(
                    surface=screen,
                    color=color,
                    rect=(
                        x * self.cell_size + self.left,
                        y * self.cell_size + self.top,
                        self.cell_size,
                        self.cell_size,
                    ),
                )
