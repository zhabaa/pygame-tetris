import pygame as pg
from typing import List, Tuple, Optional
from config import *
from figure import Figure
from utils import is_in_field


class Field:
    def __init__(self):
        """Инициализация игрового поля"""
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT
        self.grid = self._create_empty_grid()
        self.surface = None

    def _create_empty_grid(self) -> List[List[str]]:
        """Создает пустое игровое поле"""
        return [[EMPTY for _ in range(self.height)] for _ in range(self.width)]

    def reset(self) -> None:
        """Сбрасывает поле в начальное состояние"""
        self.grid = self._create_empty_grid()

    def can_place_figure(self, figure: Figure, offset_x: int = 0, offset_y: int = 0) -> bool:
        """Проверяет, можно ли разместить фигуру в указанной позиции"""
        for y, row in enumerate(figure.get_shape_matrix()):
            for x, cell in enumerate(row):
                if cell != EMPTY:
                    new_x = figure.x + x + offset_x
                    new_y = figure.y + y + offset_y
                    
                    if not (0 <= new_x < self.width and 0 <= new_y < self.height):
                        return False
                        
                    if self.grid[new_x][new_y] != EMPTY:
                        return False
        return True
    
    def checkPos(self, figure: Figure, offset_x=0, offset_y=0):
        for y, row in enumerate(figure.get_shape_matrix()):
            for x, cell in enumerate(row):
                abovecup = y + figure.y + offset_y < 0
                if abovecup or figure.current_matrix[y][x] == EMPTY:
                    continue
                if not is_in_field(x + figure.x + offset_x, y + figure.y + offset_y):
                    return False
                if self.grid[x + figure.x + offset_x][y + figure.y + offset_y] != EMPTY:
                    return False
        return True

    def merge_figure(self, figure: 'Figure') -> None:
        """Фиксирует фигуру на поле"""
        for y, row in enumerate(figure.get_shape_matrix()):
            for x, cell in enumerate(row):
                if cell != EMPTY:
                    field_x = figure.x + x
                    field_y = figure.y + y
                    if 0 <= field_x < self.width and 0 <= field_y < self.height:
                        self.grid[field_x][field_y] = figure.color

    def clear_completed_rows(self) -> int:
        """Очищает заполненные строки и возвращает их количество"""
        completed_rows = 0
        
        for y in range(self.height-1, -1, -1):
            if all(self.grid[x][y] != EMPTY for x in range(self.width)):
                self._remove_row(y)
                completed_rows += 1
                y += 1  # Проверить эту же позицию снова после сдвига
        
        return completed_rows

    def _remove_row(self, row_y: int) -> None:
        """Удаляет строку и сдвигает все вышестоящие строки вниз"""
        for y in range(row_y, 0, -1):
            for x in range(self.width):
                self.grid[x][y] = self.grid[x][y-1]
        
        # Очищаем верхний ряд
        for x in range(self.width):
            self.grid[x][0] = EMPTY

    def draw(self, surface: pg.Surface) -> None:
        """Отрисовывает игровое поле"""
        # Рамка поля
        pg.draw.rect(
            surface, 
            BORDER_COLOR,
            (
                SIDE_MARGIN - 4,
                TOP_MARGIN - 4,
                self.width * BLOCK_SIZE + 8,
                self.height * BLOCK_SIZE + 8
            ),
            5
        )
        
        # Фон поля
        pg.draw.rect(
            surface,
            FIELD_BACKGROUND,
            (
                SIDE_MARGIN,
                TOP_MARGIN,
                self.width * BLOCK_SIZE,
                self.height * BLOCK_SIZE
            )
        )
        
        # Отрисовка заполненных клеток
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] != EMPTY:
                    self._draw_block(surface, x, y, self.grid[x][y])

    def _draw_block(self, surface: pg.Surface, grid_x: int, grid_y: int, color: Tuple[int, int, int]) -> None:
        """Отрисовывает один блок"""
        pixel_x = SIDE_MARGIN + grid_x * BLOCK_SIZE
        pixel_y = TOP_MARGIN + grid_y * BLOCK_SIZE
        
        pg.draw.rect(
            surface,
            color,
            (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 1, BLOCK_SIZE - 1),
            0,
            3
        )