import pygame as pg

from game import TetrisGame
from config import WINDOW_SIZE

def main():
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Tetris")
    
    game = TetrisGame(screen)
    game.run()

if __name__ == "__main__":
    main()
