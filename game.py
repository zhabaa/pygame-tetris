import pygame as pg
import time
# import random
from typing import Tuple, Optional
from config import *
from figure import Figure
from utils import *
from field import Field
# from figuresTemplate import figures


class TetrisGame:
    def __init__(self, display: pg.Surface):
        """Initialize the Tetris game with default settings."""
        self.display = display
        self.reset_game()

        # Font initialization
        self.basic_font = pg.font.SysFont('arial', 20)
        self.big_font = pg.font.SysFont('verdana', 45)

    def reset_game(self) -> None:
        """Reset all game state variables to start a new game."""
        self.game_field = Field()
        self.score = 0
        self.level = 1
        self.fall_speed = self.calculate_fall_speed()

        # Timing controls
        self.last_move_down = time.time()
        self.last_side_move = time.time()
        self.last_fall = time.time()

        # Movement flags
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Figure management
        self.current_figure = self.get_new_figure()
        self.next_figure = self.get_new_figure()

    def run(self) -> None:
        """Main loop"""
        while True:
            self.handle_figure_spawning()
            self.handle_events()
            self.handle_movement()
            self.handle_automatic_falling()
            self.update_display()
            pg.time.Clock().tick(FPS)

    def handle_figure_spawning(self) -> None:
        """Handle spawning of new figures when needed"""
        if self.current_figure is None:
            self.current_figure = self.next_figure
            self.next_figure = self.get_new_figure()
            self.last_fall = time.time()

            if not self.game_field.checkPos(self.current_figure): ## ??? вроде фикс
                self.game_over()

    def handle_events(self) -> None:
        """Process all pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()

            self.handle_key_events(event)

    def handle_key_events(self, event: pg.event.Event) -> None:
        """Process keyboard input events."""
        if event.type == pg.KEYUP:
            self.handle_key_release(event)
        elif event.type == pg.KEYDOWN:
            self.handle_key_press(event)

    def handle_key_release(self, event: pg.event.Event) -> None:
        """Handle key release events."""
        match event.key:
            case pg.K_LEFT:
                self.moving_left = False
            case pg.K_RIGHT:
                self.moving_right = False
            case pg.K_DOWN:
                self.moving_down = False
            case _:
                pass

    def handle_key_press(self, event: pg.event.Event) -> None:
        """Handle key press events."""
        if self.current_figure is None:
            return

        match event.key:
            case pg.K_LEFT:
                self.handle_left_movement()
            case pg.K_RIGHT:
                self.handle_right_movement()
            case pg.K_DOWN:
                self.handle_soft_drop()
            case pg.K_UP:
                self.handle_rotation()
            case pg.K_RETURN:
                self.handle_hard_drop()
            case pg.K_ESCAPE:
                self.quit_game()
            case pg.K_SPACE:
                self.pause_game()
            case _:
                pass

    def handle_movement(self) -> None:
        """Handle continuous movement when keys are held down."""
        current_time = time.time()

        if (self.moving_left or self.moving_right) and current_time - self.last_side_move > SIDE_FREQ: 
            # движения в стороны
            if self.moving_left and self.game_field.checkPos(self.current_figure, offset_x=-1):
                self.current_figure.x -= 1

            elif self.moving_right and self.game_field.checkPos(self.current_figure, offset_x=1):
                self.current_figure.x += 1

            self.last_side_move = current_time

        if self.moving_down and current_time - self.last_move_down > DOWN_FREQ:
            # движение вниз
            if self.game_field.checkPos(self.current_figure, offset_y=1):
                self.current_figure.y += 1
                self.last_move_down = current_time

    def handle_automatic_falling(self) -> None:
        """Handle automatic falling of the current figure."""
        if time.time() - self.last_fall > self.fall_speed:
            if not self.game_field.checkPos(self.current_figure, offset_y=1):
                self.lock_figure()

            else:
                self.current_figure.y += 1
                self.last_fall = time.time()

    def handle_left_movement(self) -> None:
        """Обработка движения фигуры влево"""
        if self.current_figure is None:
            return

        if self.game_field.checkPos(self.current_figure, offset_x=-1):
            self.current_figure.move(-1, 0)
            self.last_side_move = time.time()

        self.moving_left = True
        self.moving_right = False

    def handle_right_movement(self) -> None:
        """Обработка движения фигуры вправо"""
        if self.current_figure is None:
            return

        if self.game_field.checkPos(self.current_figure, offset_x=1):
            self.current_figure.move(1, 0)
            self.last_side_move = time.time()

        self.moving_right = True
        self.moving_left = False

    def handle_rotation(self) -> None:
        """Обработка поворота фигуры"""
        if self.current_figure is None:
            return

        self.current_figure.rotate()

        if not self.game_field.checkPos(self.current_figure):
            self.current_figure.rotate(reverse=True)

    def handle_soft_drop(self) -> None:
        """Обработка ускоренного падения (мягкого дропа)"""
        if self.current_figure is None:
            return

        if self.game_field.checkPos(self.current_figure, offset_y=1):
            self.current_figure.move(0, 1)
            self.last_move_down = time.time()

        self.moving_down = True
        # Начисление очков за мягкий дроп можно добавить здесь

    def handle_hard_drop(self) -> None:
        """Обработка моментального падения (хард дропа)"""
        if self.current_figure is None:
            return

        # Находим максимально возможное смещение вниз
        drop_distance = 0

        while self.game_field.checkPos(self.current_figure, offset_y=drop_distance + 1):
            drop_distance += 1

        if drop_distance > 0:
            self.current_figure.move(0, drop_distance)
            self.lock_figure()
            self.score += drop_distance * 2
        
        self.current_figure = self.next_figure
        self.next_figure = self.get_new_figure() # вроде фиксит README.md 

    def lock_figure(self) -> None:
        """Lock the current figure in place and check for completed lines."""
        self.game_field.merge_figure(self.current_figure)
        lines_cleared = self.game_field.clear_completed_rows()
        self.update_score(lines_cleared)
        self.current_figure = None

    def update_score(self, lines_cleared: int) -> None:
        """Update score and level based on cleared lines."""
        if lines_cleared > 0:
            self.score += lines_cleared * 100
            self.level = self.score // 10_000 + 0.2
            self.fall_speed = self.calculate_fall_speed()

    def calculate_fall_speed(self) -> float:
        """Calculate fall speed based on current level."""
        return max(0.05, BASE_FALL_SPEED + (self.level * 0.02))

    def get_new_figure(self) -> Figure:
        """Generate a new random figure."""
        return Figure(int(FIELD_WIDTH / 2) - 2, -2)

    def update_display(self) -> None:
        """Update all visual elements on the screen."""
        self.display.fill(BACKGROUND_COLOR)
        self.draw_game_border()
        self.draw_game_field()
        self.draw_ui()

        if self.current_figure is not None:
            self.draw_figure(self.current_figure)

        pg.display.update()

    def draw_game_border(self) -> None:
        """Draw the border around the game field."""
        border_rect = (
            SIDE_MARGIN - 4, 
            TOP_MARGIN - 4,
            FIELD_WIDTH * BLOCK_SIZE + 8,
            FIELD_HEIGHT * BLOCK_SIZE + 8
        )
        pg.draw.rect(self.display, BORDER_COLOR, border_rect, 5)

    def draw_game_field(self) -> None:
        """Draw all blocks in the game field."""
        field_rect = (
            SIDE_MARGIN,
            TOP_MARGIN,
            FIELD_WIDTH * BLOCK_SIZE,
            FIELD_HEIGHT * BLOCK_SIZE
        )
        pg.draw.rect(self.display, FIELD_BACKGROUND, field_rect)

        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                if self.game_field.grid[x][y] != EMPTY:
                    self.draw_block(x, y, self.game_field.grid[x][y])

    def draw_ui(self) -> None:
        """Draw all UI elements."""
        self.draw_title()
        self.draw_score_info()
        self.draw_next_figure_preview()
        self.draw_controls_info()

    def draw_figure(self, figure: Figure, pixel_x: Optional[int] = None, pixel_y: Optional[int] = None) -> None:
        """Draw a figure at the specified position."""
        shape_matrix = figure.get_shape_matrix()

        if pixel_x is None and pixel_y is None:
            pixel_x, pixel_y = convert_block_to_pixel(figure.x, figure.y)

        for y, row in enumerate(shape_matrix):
            for x, cell in enumerate(row):
                if cell != EMPTY:
                    block_x = pixel_x + x * BLOCK_SIZE
                    block_y = pixel_y + y * BLOCK_SIZE
                    self.draw_block(None, None, figure.color, block_x, block_y)

    def draw_block(self, grid_x: Optional[int], grid_y: Optional[int], color: Tuple[int, int, int], 
                  pixel_x: Optional[int] = None, pixel_y: Optional[int] = None) -> None:
        """Draw a single block at specified coordinates."""
        if color == EMPTY:
            return

        if pixel_x is None or pixel_y is None:
            pixel_x, pixel_y = convert_block_to_pixel(grid_x, grid_y)

        block_rect = (pixel_x + 1, pixel_y + 1, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
        pg.draw.rect(self.display, color, block_rect, 0, 3)

    def draw_title(self) -> None:
        """Draw the game title."""
        draw_text(
            surface=self.display,
            font=self.big_font,
            text="Tetris",
            x=WINDOW_WIDTH // 2,
            y=50,
            alignment="center",
            color=TITLE_COLOR
        )

    def draw_score_info(self) -> None:
        """Draw score and level information."""
        draw_text(
            self.display, self.basic_font,
            f"Score: {self.score}",
            WINDOW_WIDTH * 0.1, 180,
            "topleft", color=TEXT_COLOR
        )
        draw_text(
            self.display, self.basic_font,
            f"Level: {self.level}",
            WINDOW_WIDTH * 0.1, 220,
            "topleft", color=TEXT_COLOR
        )

    def draw_next_figure_preview(self) -> None:
        """Draw the next figure preview."""
        draw_text(
            self.display, self.basic_font,
            "Next:",
            WINDOW_WIDTH * 0.7, 180,
            "topleft", color=TEXT_COLOR
        )
        self.draw_figure(
            self.next_figure,
            pixel_x=WINDOW_WIDTH * 0.7,
            pixel_y=230
        )

    def draw_controls_info(self) -> None:
        """Draw control information."""
        draw_text(
            self.display,
            self.basic_font,
            "Controls:",
            WINDOW_WIDTH * 0.1,
            380,
            "topleft",
            color=TEXT_COLOR,
        )
        draw_text(
            self.display,
            self.basic_font,
            "Move: Arrow Keys",
            WINDOW_WIDTH * 0.1,
            420,
            "topleft",
            color=TEXT_COLOR,
        )
        draw_text(
            self.display,
            self.basic_font,
            "Rotate: Up Arrow",
            WINDOW_WIDTH * 0.1,
            440,
            "topleft",
            color=TEXT_COLOR,
        )
        draw_text(
            self.display,
            self.basic_font,
            "Pause: Space",
            WINDOW_WIDTH * 0.1,
            460,
            "topleft",
            color=TEXT_COLOR,
        )
        draw_text(
            self.display,
            self.basic_font,
            "Quit: Esc",
            WINDOW_WIDTH * 0.1,
            480,
            "topleft",
            color=TEXT_COLOR,
        )

    def game_over(self) -> None:
        """Handle game over condition."""
        self.show_message("Game Over")
        time.sleep(2)
        self.reset_game()

    def pause_game(self) -> None:
        """Pause the game and show pause screen."""
        self.show_message("Paused")
        self.last_fall = time.time()
        self.last_move_down = time.time()
        self.last_side_move = time.time()

    def show_message(self, text: str) -> None:
        """Display a centered message on the screen."""
        overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.display.blit(overlay, (0, 0))

        draw_text(
            self.display, self.big_font,
            text,
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
            "center", color=TEXT_COLOR
        )

        pg.display.update()
        self.wait_for_key_press()

    def wait_for_key_press(self) -> None:
        """Wait for any key press."""
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game()
                elif event.type == pg.KEYDOWN:
                    waiting = False
            pg.time.Clock().tick(FPS)

    def quit_game(self) -> None:
        """Cleanly exit the game."""
        pg.quit()
        raise SystemExit
