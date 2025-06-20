from config import side_margin, top_margin, block

def calcSpeed(points):
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed



def convertCoords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))


def createTextObject(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()