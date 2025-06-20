# config.py
# import pygame #Раскомментируйте если используете pygame

fps = 25

window_size = window_w, window_h = (600, 500)
block, cup_h, cup_w = 20, 20, 10

side_freq, down_freq = 0.15, 0.1

side_margin = int((window_w - cup_w * block) / 2)
top_margin = window_h - (cup_h * block) - 5


# basic_font = pygame.font.SysFont('arial', 20) #Раскомментируйте если используете pygame
# big_font = pygame.font.SysFont('verdana', 45) #Раскомментируйте если используете pygame

# Цвета
white = (255, 255, 255)
gray = (185, 185, 185)
black = (0, 0, 0)
colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))

# Цвета элементов интерфейса
brd_color = white
bg_color = black
txt_color = white
title_color = colors[3]
info_color = colors[0]


# Размеры фигур
figure_width, figure_height = 5, 5
empty = 'o'  # Используем строку 'o' для обозначения пустого места


# Формы фигур (Тетрис)
figures = {
    "S": [
        ["ooooo", "ooooo", "ooxxo", "oxxoo", "ooooo"],
        ["ooooo", "ooxoo", "ooxxo", "oooxo", "ooooo"],
    ],
    "Z": [
        ["ooooo", "ooooo", "oxxoo", "ooxxo", "ooooo"],
        ["ooooo", "ooxoo", "oxxoo", "oxooo", "ooooo"],
    ],
    "J": [
        ["ooooo", "oxooo", "oxxxo", "ooooo", "ooooo"],
        ["ooooo", "ooxxo", "ooxoo", "ooxoo", "ooooo"],
        ["ooooo", "ooooo", "oxxxo", "oooxo", "ooooo"],
        ["ooooo", "ooxoo", "ooxoo", "oxxoo", "ooooo"],
    ],
    "L": [
        ["ooooo", "oooxo", "oxxxo", "ooooo", "ooooo"],
        ["ooooo", "ooxoo", "ooxoo", "ooxxo", "ooooo"],
        ["ooooo", "ooooo", "oxxxo", "oxooo", "ooooo"],
        ["ooooo", "oxxoo", "ooxoo", "ooxoo", "ooooo"],
    ],
    "I": [
        ["ooxoo", "ooxoo", "ooxoo", "ooxoo", "ooooo"],
        ["ooooo", "ooooo", "xxxxo", "ooooo", "ooooo"],
    ],
    "O": [["ooooo", "ooooo", "oxxoo", "oxxoo", "ooooo"]],
    "T": [
        ["ooooo", "ooxoo", "oxxxo", "ooooo", "ooooo"],
        ["ooooo", "ooxoo", "ooxxo", "ooxoo", "ooooo"],
        ["ooooo", "ooooo", "oxxxo", "ooxoo", "ooooo"],
        ["ooooo", "ooxoo", "oxxoo", "ooxoo", "ooooo"],
    ],
}