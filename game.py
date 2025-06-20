# game.py
import pygame as pg
import time
from config import *
from figure import Figure
from utils import emptycup, checkPos, addToCup, clearCompleted
import random

class TetrisGame:
    def __init__(self, display_surf):
        self.display_surf = display_surf
        self.cup = emptycup()
        self.last_move_down = time.time()
        self.last_side_move = time.time()
        self.last_fall = time.time()
        self.going_down = False
        self.going_left = False
        self.going_right = False
        self.points = 0
        self.level, self.fall_speed = self.calcSpeed(self.points)
        self.fallingFig = self.getNewFig()
        self.nextFig = self.getNewFig()
        self.basic_font = pg.font.SysFont('arial', 20)
        self.big_font = pg.font.SysFont('verdana', 45)

    def run(self):
        while True:
            if self.fallingFig is None:
                self.fallingFig = self.nextFig
                self.nextFig = self.getNewFig()
                self.last_fall = time.time()

                if not checkPos(self.cup, self.fallingFig):
                    return  # Game Over

            self.handle_events()

            # Управление падением фигуры при удержании клавиш
            if (self.going_left or self.going_right) and time.time() - self.last_side_move > side_freq:
                if self.going_left and checkPos(self.cup, self.fallingFig, adjX=-1):
                    self.fallingFig.x -= 1
                elif self.going_right and checkPos(self.cup, self.fallingFig, adjX=1):
                    self.fallingFig.x += 1
                self.last_side_move = time.time()

            if self.going_down and time.time() - self.last_move_down > down_freq and checkPos(self.cup, self.fallingFig, adjY=1):
                self.fallingFig.y += 1
                self.last_move_down = time.time()

            if time.time() - self.last_fall > self.fall_speed:  # Свободное падение фигуры
                if not checkPos(self.cup, self.fallingFig, adjY=1):
                    addToCup(self.cup, self.fallingFig)
                    self.points += clearCompleted(self.cup)
                    self.level, self.fall_speed = self.calcSpeed(self.points)
                    self.fallingFig = None
                else:
                    self.fallingFig.y += 1
                    self.last_fall = time.time()

            self.draw()
            pg.display.update()
            pg.time.Clock().tick(fps)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.pauseScreen()
                    self.showText('Пауза')
                    self.last_fall = time.time()
                    self.last_move_down = time.time()
                    self.last_side_move = time.time()
                elif event.key == pg.K_LEFT:
                    self.going_left = False
                elif event.key == pg.K_RIGHT:
                    self.going_right = False
                elif event.key == pg.K_DOWN:
                    self.going_down = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and checkPos(self.cup, self.fallingFig, adjX=-1):
                    self.fallingFig.x -= 1
                    self.going_left = True
                    self.going_right = False
                    self.last_side_move = time.time()

                elif event.key == pg.K_RIGHT and checkPos(self.cup, self.fallingFig, adjX=1):
                    self.fallingFig.x += 1
                    self.going_right = True
                    self.going_left = False
                    self.last_side_move = time.time()

                elif event.key == pg.K_UP:
                    self.fallingFig.rotation = (self.fallingFig.rotation + 1) % len(figures[self.fallingFig.shape])
                    if not checkPos(self.cup, self.fallingFig):
                        self.fallingFig.rotation = (self.fallingFig.rotation - 1) % len(figures[self.fallingFig.shape])

                elif event.key == pg.K_DOWN:
                    self.going_down = True
                    if checkPos(self.cup, self.fallingFig, adjY=1):
                        self.fallingFig.y += 1
                    self.last_move_down = time.time()

                elif event.key == pg.K_RETURN:
                    self.going_down = False
                    self.going_left = False
                    self.going_right = False
                    for i in range(1, cup_h):
                        if not checkPos(self.cup, self.fallingFig, adjY=i):
                            break
                    self.fallingFig.y += i - 1
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

    def calcSpeed(self, points):
        level = int(points / 10) + 1
        fall_speed = 0.27 - (level * 0.02)
        return level, fall_speed

    def getNewFig(self):
        shape = random.choice(list(figures.keys()))
        return Figure(int(cup_w / 2) - int(fig_w / 2), -2, shape)

    def draw(self):
        self.display_surf.fill(bg_color)
        self.drawTitle()
        self.gamecup()
        self.drawInfo(self.points, self.level)
        self.drawnextFig()
        if self.fallingFig is not None:
            self.drawFig(self.fallingFig)

    def pauseScreen(self):
        pause = pg.Surface((600, 500), pg.SRCALPHA)
        pause.fill((0, 0, 255, 127))
        self.display_surf.blit(pause, (0, 0))

    def showText(self, text):
        titleSurf, titleRect = self.txtObjects(text, self.big_font, title_color)
        titleRect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
        self.display_surf.blit(titleSurf, titleRect)

        pressKeySurf, pressKeyRect = self.txtObjects('Нажмите любую клавишу для продолжения', self.basic_font, title_color)
        pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
        self.display_surf.blit(pressKeySurf, pressKeyRect)

        while True:
            event = pg.event.wait()
            if event.type == pg.KEYDOWN:
                return
            pg.display.update()
            pg.time.Clock().tick()

    def txtObjects(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()

    def gamecup(self):
        # граница игрового поля-стакана
        pg.draw.rect(self.display_surf, brd_color, (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8), 5)

        # фон игрового поля
        pg.draw.rect(self.display_surf, bg_color, (side_margin, top_margin, block * cup_w, block * cup_h))
        for x in range(cup_w):
            for y in range(cup_h):
                self.drawBlock(x, y, self.cup[x][y])

    def drawTitle(self):
        titleSurf = self.big_font.render('Тетрис Lite', True, title_color)
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (window_w - 425, 30)
        self.display_surf.blit(titleSurf, titleRect)

    def drawInfo(self, points, level):
        pointsSurf = self.basic_font.render(f'Баллы: {points}', True, txt_color)
        pointsRect = pointsSurf.get_rect()
        pointsRect.topleft = (window_w - 550, 180)
        self.display_surf.blit(pointsSurf, pointsRect)

        levelSurf = self.basic_font.render(f'Уровень: {level}', True, txt_color)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (window_w - 550, 250)
        self.display_surf.blit(levelSurf, levelRect)

        pausebSurf = self.basic_font.render('Пауза: пробел', True, info_color)
        pausebRect = pausebSurf.get_rect()
        pausebRect.topleft = (window_w - 550, 420)
        self.display_surf.blit(pausebSurf, pausebRect)

        escbSurf = self.basic_font.render('Выход: Esc', True, info_color)
        escbRect = escbSurf.get_rect()
        escbRect.topleft = (window_w - 550, 450)
        self.display_surf.blit(escbSurf, escbRect)

    def drawFig(self, fig, pixelx=None, pixely=None):
        figToDraw = figures[fig.shape][fig.rotation]
        if pixelx is None and pixely is None:
            pixelx, pixely = self.convertCoords(fig.x, fig.y)

        #отрисовка элементов фигур
        for x in range(fig_w):
            for y in range(fig_h):
                if figToDraw[y][x] != empty:
                    self.drawBlock(x=None, y=None, color=fig.color, pixelx=pixelx + (x * block), pixely=pixely + (y * block))

    def drawnextFig(self, pixelx=None, pixely=None):  # превью следующей фигуры
        nextSurf = self.basic_font.render('Следующая:', True, txt_color)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (window_w - 150, 180)
        self.display_surf.blit(nextSurf, nextRect)
        self.drawFig(self.nextFig, pixelx=window_w-150, pixely=230)

    def convertCoords(self, block_x, block_y):
        return (side_margin + (block_x * block)), (top_margin + (block_y * block))

    def drawBlock(self, x, y, color, pixelx=None, pixely=None):
        #отрисовка квадратных блоков, из которых состоят фигуры
        if color == empty:
            return
        if pixelx is None and pixely is None:
            pixelx, pixely = self.convertCoords(x, y)

        pg.draw.rect(self.display_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
        pg.draw.rect(self.display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
        pg.draw.circle(self.display_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)