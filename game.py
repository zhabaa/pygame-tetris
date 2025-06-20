import pygame
from pygame.locals import *
import sys

from config import *
from functions import createTextObject, calcSpeed, convertCoords
from field import Field
from figure import Figure
import time

pygame.font.init()
basic_font = pygame.font.Font("./static/font/GNF.ttf", 20)
big_font = pygame.font.Font('./static/font/GNF.ttf', 45)


class Tetris:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Тетрис Lite')

        self.fps_clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode(window_size)
        self.field = Field()
        
        self.last_fall = time.time()

        self.points = 0
        self.level, self.fall_speed = calcSpeed(self.points)

    def dropgame(self):  # Исправлена опечатка
        pygame.quit()
        sys.exit()

    def drawInfo(self, points, level):
        pointsSurf = basic_font.render(f'Баллы: {points}', True, txt_color)
        pointsRect = pointsSurf.get_rect()
        pointsRect.topleft = (window_w - 550, 180)

        levelSurf = basic_font.render(f'Уровень: {level}', True, txt_color)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (window_w - 550, 250)

        pausebSurf = basic_font.render('Пауза: пробел', True, info_color)
        pausebRect = pausebSurf.get_rect()
        pausebRect.topleft = (window_w - 550, 420)

        escbSurf = basic_font.render('Выход: Esc', True, info_color)
        escbRect = escbSurf.get_rect()
        escbRect.topleft = (window_w - 550, 450)

        self.display_surface.blit(pointsSurf, pointsRect)
        self.display_surface.blit(levelSurf, levelRect)
        self.display_surface.blit(pausebSurf, pausebRect)
        self.display_surface.blit(escbSurf, escbRect)

    def pauseScreen(self):
        pause = pygame.Surface((600, 500), pygame.SRCALPHA)
        pause.fill((0, 0, 255, 128))
        self.display_surface.blit(pause, (0, 0))

        self.showTextOnScreen('Пауза')

    def showTextOnScreen(self, text):
        titleSurf, titleRect = createTextObject(text, big_font, title_color)
        titleRect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)

        self.display_surface.blit(titleSurf, titleRect)

        pressKeySurf, pressKeyRect = createTextObject(
            "Нажмите любую клавишу для продолжения", basic_font, title_color
        )
        pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
        self.display_surface.blit(pressKeySurf, pressKeyRect)

        while self.checkKeys() is None:
            pygame.display.update()
            self.fps_clock.tick()

    def drawTitle(self):
        titleSurf = big_font.render("Тетрис Lite", True, title_color)
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (window_w - 425, 30)
        self.display_surface.blit(titleSurf, titleRect)

    def quitGame(self):
        quit_flag = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit_flag = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    quit_flag = True

        if quit_flag:
            self.dropgame()

        pygame.event.clear()

    def checkKeys(self):
        self.quitGame()

        events = pygame.event.get([pygame.KEYDOWN, pygame.KEYUP])
        for event in events:
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):  # Обрабатываем оба типа событий
                return event.key

        return None

    def runTetris(self):
        activeFigure = Figure()
        nextFigure = Figure()

        last_move_down = time.time()
        last_side_move = time.time()

        while True:
            if activeFigure is None:
                activeFigure = nextFigure
                nextFigure = Figure()

                self.last_fall = time.time()

                if not self.field.checkPos(activeFigure):
                    return

            self.quitGame()

            events = pygame.event.get()
            for event in events:
                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.pauseScreen()
                    elif event.key == K_LEFT:
                        activeFigure.going_left = False
                    elif event.key == K_RIGHT:
                        activeFigure.going_right = False
                    elif event.key == K_DOWN:
                        activeFigure.going_down = False

                elif event.type == KEYDOWN:
                    if event.key == K_LEFT and self.field.checkPos(activeFigure, adjX=-1):
                        activeFigure.x -= 1
                        activeFigure.going_left = True
                        activeFigure.going_right = False
                        last_side_move = time.time()

                    elif event.key == K_RIGHT and self.field.checkPos(activeFigure, adjX=1):
                        activeFigure.x += 1  # Исправлено: activeFigure.x += 1
                        activeFigure.going_right = True
                        activeFigure.going_left = False
                        last_side_move = time.time()

                    elif event.key == K_UP:
                        new_rotation = (activeFigure.rotation + 1) % len(figures[activeFigure.shape])
                        activeFigure.rotation = new_rotation
                        activeFigure.field = figures[activeFigure.shape][activeFigure.rotation]
                        if not self.field.checkPos(activeFigure):
                            activeFigure.rotation = (activeFigure.rotation - 1) % len(figures[activeFigure.shape])
                            activeFigure.field = figures[activeFigure.shape][activeFigure.rotation]

                    elif event.key == K_DOWN:
                        activeFigure.going_down = True
                        if self.field.checkPos(activeFigure, adjY=1):
                            activeFigure.y += 1

                        last_move_down = time.time()

                    elif event.key == K_RETURN:
                        while self.field.checkPos(activeFigure, adjY=1):
                            activeFigure.y += 1

            if (activeFigure.going_left or activeFigure.going_right) and time.time() - last_side_move > side_freq:
                if activeFigure.going_left and self.field.checkPos(activeFigure, adjX=-1):
                    activeFigure.x -= 1

                elif activeFigure.going_right and self.field.checkPos(activeFigure, adjX=1):
                    activeFigure.x += 1

                last_side_move = time.time()

            if activeFigure.going_down and time.time() - last_move_down > down_freq and self.field.checkPos(activeFigure, adjY=1):
                activeFigure.y += 1
                last_move_down = time.time()

            if time.time() - self.last_fall > self.fall_speed:
                if not self.field.checkPos(activeFigure, adjY=1):
                    self.field.addFigure(activeFigure)
                    removed_lines = self.field.clearCompletedRow()
                    self.points += removed_lines
                    self.level, self.fall_speed = calcSpeed(self.points)
                    activeFigure = None
                else:
                    activeFigure.y += 1
                    self.last_fall = time.time()

            # рисуем окно игры со всеми надписями
            self.display_surface.fill(bg_color)
            self.drawTitle()
            self.drawField()
            self.drawInfo(self.points, self.level)
            self.drawnextFig(nextFigure)
            if activeFigure is not None:
                self.drawFig(activeFigure)
            pygame.display.update()
            self.fps_clock.tick(fps)

    def drawField(self):
        # граница игрового поля
        pygame.draw.rect(
            self.display_surface,
            brd_color,
            (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8),
            5,
        )

        # фон игрового поля
        pygame.draw.rect(
            self.display_surface, bg_color, (side_margin, top_margin, block * cup_w, block * cup_h)
        )
        for x in range(cup_w):
            for y in range(cup_h):
                self.drawBlock(x, y, self.field.field[x][y]) # Исправлено: доступ к полю field

    def drawBlock(self, block_x, block_y, color, pixelx=None, pixely=None):
        # отрисовка квадратных блоков
        if color == empty:
            return
        if pixelx is None and pixely is None:
            pixelx, pixely = convertCoords(block_x, block_y)

        pygame.draw.rect(
            self.display_surface,
            colors[color],
            (pixelx + 1, pixely + 1, block - 1, block - 1),
            0,
            3,
        )
        pygame.draw.rect(
            self.display_surface,
            lightcolors[color],
            (pixelx + 1, pixely + 1, block - 4, block - 4),
            0,
            3,
        )
        pygame.draw.circle(
            self.display_surface, colors[color], (pixelx + block / 2, pixely + block / 2), 5
        )

    def drawFig(self, figure, pixelx=None, pixely=None):
        figToDraw = figure.field # Исправлено: figure.field
        if pixelx is None and pixely is None:
            pixelx, pixely = convertCoords(figure.x, figure.y)

        for x in range(figure_width):
            for y in range(figure_height):
                if figToDraw[y][x] != empty:
                    # Нам не нужно преобразовывать None в координаты, потому что они уже заданы явно
                    self.drawBlock(
                        None,
                        None,
                        figure.color,
                        pixelx + (x * block),
                        pixely + (y * block),
                    )

    def drawnextFig(self, figure):  # превью следующей фигуры
        nextSurf = basic_font.render("Следующая:", True, txt_color)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (window_w - 150, 180)
        self.display_surface.blit(nextSurf, nextRect)
        self.drawFig(figure, pixelx=window_w - 150, pixely=230)

    def start(self):
        self.showTextOnScreen('Тетрис Lite')

        while True:
            self.runTetris()
            self.pauseScreen()
            self.showTextOnScreen('Игра закончена')


if __name__ == "__main__":
    game = Tetris()
    game.start()