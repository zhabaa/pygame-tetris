import pygame

from config import (
    FIELD_WIDTH,
    FIELD_HEIGHT,
    BLOCK_SIZE,
    SIDE_MARGIN,
    TOP_MARGIN,
    COLORS,
)

def is_in_field(x, y):
    return 0 <= x < FIELD_WIDTH and y < FIELD_HEIGHT


def convert_block_to_pixel(block_x: int, block_y: int) -> tuple[int, int]:
    """Конвертирует координаты блоков в пиксельные координаты на экране"""
    pixel_x = SIDE_MARGIN + block_x * BLOCK_SIZE
    pixel_y = TOP_MARGIN + block_y * BLOCK_SIZE
    return (pixel_x, pixel_y)


def draw_text(surface: pygame.Surface, font: pygame.font.Font, text: str, x: int, y: int, alignment: str = "topleft", *, antialias: bool = True, color: tuple[int, int, int] = COLORS["white"], background: tuple[int, int, int] | None = None,
) -> pygame.Rect:
    """Рендерит текст на поверхности с указанным выравниванием"""

    text_surface = font.render(text, antialias, color, background)
    text_rect = text_surface.get_rect()

    alignment_methods = {
        "topleft": "topleft",
        "topright": "topright",
        "midtop": "midtop",
        "center": "center",
        "midbottom": "midbottom",
        "bottomleft": "bottomleft",
        "bottomright": "bottomright",
    }

    setattr(text_rect, alignment_methods[alignment], (x, y))
    
    # Проверка для ебланов
    # try:
    #     setattr(text_rect, alignment_methods[alignment], (x, y))
    # except KeyError:
    #     raise ValueError(
    #         f"Unsupported alignment: {alignment}. "
    #         f"Supported values are: {', '.join(alignment_methods.keys())}"
    #     )

    surface.blit(text_surface, text_rect)
    return text_rect
