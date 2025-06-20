from config import empty, cup_w, cup_h, figure_width, figure_height
from figure import Figure


class Field:
    def __init__(self):
        self.field = [[empty] * cup_h for _ in range(cup_w)]

    def changeField(self, x, y, state):
        self.field[x][y] = state # Исправлено: индексация списка

    def isInField(self, x, y):
        return 0 <= x < cup_w and 0 <= y < cup_h # Добавлена проверка y >= 0

    def addFigure(self, figure: Figure):
        for x in range(figure_width):
            for y in range(figure_height):
                if figure.field[x][y] != empty: # Проверяем блок фигуры, а не позицию
                    self.field[x + figure.x][y + figure.y] = figure.field[x][y] # Копируем цвет из фигуры

    def checkPos(self, figure: Figure, adjX=0, adjY=0):
        for x in range(figure_width):
            for y in range(figure_height):

                isAboveCup = (y + figure.y + adjY) < 0

                if isAboveCup or figure.field[x][y] == empty: # Проверяем блок фигуры, а не позицию
                    continue

                dx = x + figure.x + adjX
                dy = y + figure.y + adjY

                if not self.isInField(dx, dy) or self.field[dx][dy] != empty: # Исправлено: проверка нахождения в поле и занятости
                    return False

        return True

    def isCompletedRow(self, y):
        for x in range(cup_w):
            if self.field[x][y] == empty:
                return False

        return True

    def clearCompletedRow(self):
        removed_lines = 0
        y = cup_h - 1

        while y >= 0:
            if self.isCompletedRow(y):
                # Сдвигаем все строки выше текущей вниз
                for pushDownY in range(y, 0, -1):
                    for x in range(cup_w):
                        self.field[x][pushDownY] = self.field[x][pushDownY - 1]

                # Очищаем верхнюю строку
                for x in range(cup_w):
                    self.field[x][0] = empty

                removed_lines += 1

            else:
                y -= 1

        return removed_lines