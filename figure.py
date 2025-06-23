import random
from figuresTemplate import figures


class Figure:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.shape_type = random.choice(list(figures.keys()))
        self.rotations = figures[self.shape_type][0]
        self.color = figures[self.shape_type][1]

        self.current_rotation_index = random.randint(0, len(self.rotations) - 1)
        self.current_matrix = self.rotations[self.current_rotation_index]

    def get_shape_matrix(self) -> list[list]:
        """Возвращает текущую матрицу фигуры."""
        return self.current_matrix

    def rotate(self, reverse: bool = False) -> None:
        """Поворачивает фигуру на следующее состояние."""
        state = 1 if not reverse else -1
        self.current_rotation_index = (self.current_rotation_index + state) % len(self.rotations)
        self.current_matrix = self.rotations[self.current_rotation_index]

    def rotate_back(self) -> None:
        """Откатывает поворот фигуры"""
        self.current_rotation_index = (self.current_rotation_index - 1) % len(
            self.rotations
        )
        self.current_matrix = self.rotations[self.current_rotation_index]

    def move(self, dx: int, dy: int) -> None:
        """Перемещает фигуру на указанное смещение"""
        self.x += dx
        self.y += dy

    def __repr__(self) -> str:
        """Строковое представление фигуры"""
        return "\n".join(self.current_matrix)
