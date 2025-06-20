# graphics.py
import pygame as pg
from config import *

def drawBlock(surface, block_x, block_y, color, pixelx=None, pixely=None):
    #отрисовка квадратных блоков, из которых состоят фигуры
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(surface, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pg.draw.rect(surface, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pg.draw.circle(surface, colors[color], (pixelx + block / 2, pixely + block / 2), 5)

def gamecup(surface, cup):
    # граница игрового поля-стакана
    pg.draw.rect(surface, brd_color, (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8), 5)

    # фон игрового поля
    pg.draw.rect(surface, bg_color, (side_margin, top_margin, block * cup_w, block * cup_h))
    for x in range(cup_w):
        for y in range(cup_h):
            drawBlock(surface, x, y, cup[x][y])

def drawTitle(surface, big_font, title_color):
    titleSurf = big_font.render('Тетрис Lite', True, title_color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (window_w - 425, 30)
    surface.blit(titleSurf, titleRect)

def drawInfo(surface, basic_font, txt_color, info_color, points, level):
    pointsSurf = basic_font.render(f'Баллы: {points}', True, txt_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_w - 550, 180)
    surface.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Уровень: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 550, 250)
    surface.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Пауза: пробел', True, info_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (window_w - 550, 420)
    surface.blit(pausebSurf, pausebRect)

    escbSurf = basic_font.render('Выход: Esc', True, info_color)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (window_w - 550, 450)
    surface.blit(escbSurf, escbRect)

def drawFig(surface, fig, figures, empty, colors, block, pixelx=None, pixely=None):
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])

    #отрисовка элементов фигур
    for x in range(5):
        for y in range(5):
            if figToDraw[y][x] != empty:
                drawBlock(surface, None, None, colors[fig['color']], pixelx + (x * block), pixely + (y * block))

def drawnextFig(surface, fig, basic_font, txt_color, figures, empty, colors, block):  # превью следующей фигуры
    nextSurf = basic_font.render('Следующая:', True, txt_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_w - 150, 180)
    surface.blit(nextSurf, nextRect)
    drawFig(surface, fig, figures, empty, colors, block, pixelx=window_w-150, pixely=230)

def convertCoords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))