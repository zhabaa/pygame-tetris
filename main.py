# main.py
import pygame as pg
from game import TetrisGame
from config import window_w, window_h

def main():
    pg.init()
    display_surf = pg.display.set_mode((window_w, window_h))
    pg.display.set_caption('Тетрис Lite')

    game = TetrisGame(display_surf)
    game.showText('Тетрис Lite')
    while True:
        game.run()
        game.pauseScreen()
        game.showText('Игра закончена')

if __name__ == '__main__':
    main()