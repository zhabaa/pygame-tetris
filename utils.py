# utils.py
from config import cup_w, cup_h, fig_w, fig_h, empty, figures

def emptycup():
    # создает пустой стакан
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup

def incup(x, y):
    return x >= 0 and x < cup_w and y < cup_h

def checkPos(cup, fig, adjX=0, adjY=0):
    # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
    for x in range(fig_w):
        for y in range(fig_h):
            abovecup = y + fig.y + adjY < 0
            if abovecup or figures[fig.shape][fig.rotation][y][x] == empty:
                continue
            if not incup(x + fig.x + adjX, y + fig.y + adjY):
                return False
            if cup[x + fig.x + adjX][y + fig.y + adjY] != empty:
                return False
    return True

def isCompleted(cup, y):
    # проверяем наличие полностью заполненных рядов
    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True

def clearCompleted(cup):
    # Удаление заполенных рядов и сдвиг верхних рядов вниз
    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if isCompleted(cup, y):
           for pushDownY in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][pushDownY] = cup[x][pushDownY-1]
           for x in range(cup_w):
                cup[x][0] = empty
           removed_lines += 1
        else:
            y -= 1
    return removed_lines

def addToCup(cup, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig.shape][fig.rotation][y][x] != empty:
                cup[x + fig.x][y + fig.y] = fig.color