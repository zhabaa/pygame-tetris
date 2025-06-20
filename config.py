# config.py
import pygame as pg

# Основные параметры
fps = 25
window_w, window_h = 600, 500
block, cup_h, cup_w = 20, 20, 10

side_freq, down_freq = 0.15, 0.1

side_margin = int((window_w - cup_w * block) / 2)
top_margin = window_h - (cup_h * block) - 5

# Цвета
colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))
white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)
brd_color, bg_color, txt_color, title_color, info_color = (
    white,
    black,
    white,
    colors[3],
    colors[0],
)

# Фигуры
fig_w, fig_h = 5, 5
empty = "o"

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
