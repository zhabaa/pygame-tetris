FPS = 20
SIDE_FREQ, DOWN_FREQ = 0.15, 0.1

BASE_FALL_SPEED = 0.1

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

BLOCK = BLOCK_SIZE = 20
BLOCK_WIDTH, BLOCK_HEIGHT = 5, 5

FIELD_HEIGHT, FIELD_WIDTH = 20, 10

SIDE_MARGIN = int((WINDOW_WIDTH - FIELD_WIDTH * BLOCK) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (FIELD_HEIGHT * BLOCK) - 5

EMPTY = "."

COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
}

BLOCK_COLORS = {
    "Pink": (240, 192, 203),
    "Lavender": (224, 208, 244),
    "Mint": (204, 255, 204),
    "Blue": (190, 218, 255),
    "Peach": (255, 218, 185),
    "Lemon": (255, 255, 224),
    "Seafoam": (178, 255, 204)
}

BORDER_COLOR = COLORS['white']
FIELD_BACKGROUND = COLORS['black']
BACKGROUND_COLOR = COLORS['black']

TITLE_COLOR = COLORS['white']
TEXT_COLOR = COLORS['white']
