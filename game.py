import random
import pygame as pg
from settings import COLORS, SIZE, FPS
from board import Board
from blocks import S_Block, T_Block, ZL_Block, ZR_Block, Hero_Block, LL_Block, LR_Block


class Game:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SIZE)
        self.blocks = list()

    def run(self):

        clock = pg.time.Clock()
        clock.tick()

        board = Board(10, 22)
        board.set_view(150, 50, 30)

        block = LL_Block(4, 0)
        
        self.blocks.append(block)

        running = True

        while running:
            clock.tick(FPS)
            self.screen.fill(COLORS['Black'])
            board.render(self.screen)
            board.draw_blocks(self.screen, self.blocks)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    for block in self.blocks:
                        block.move(event.key)

                    # if event.key == pg.K_UP:

            for block in self.blocks:
                block.fall()


            # if not block.is_moving:
            #     block = random.choice()

            pg.display.flip()
        pg.quit()
