import numpy as np
from typing import List, Tuple
from constants import *
from engine import Engine
from tetromino import Tetromino

class Board:
    height: int = GRID_HEIGHT
    width: int = GRID_WIDTH
    prev_grid: List[List[Tuple[int, int, int]]]
    grid: List[List[Tuple[int, int, int]]]
    curr_tetromino: Tetromino
    score: int
    game_over: bool

    def __init__(self):
        self.clear()

    def clear(self):
        self.prev_grid = np.full((self.height, self.width, 3),
                            BLACK, dtype = object).tolist()
        self.grid = np.full((self.height, self.width, 3),
                            BLACK, dtype = object).tolist()
        self.score = 0
        self.game_over = False
        self.spawn_tetromino()


    def spawn_tetromino(self):
        if not self.change_curr_tetromino(Tetromino()):
            self.game_over = True

    def change_curr_tetromino(self, tetromino: Tetromino) -> bool:
        if not self.tetromino_position_is_valid(tetromino):
            return False

        self.update_grid(tetromino)
        return True


    def tetromino_position_is_valid(self, tetromino: Tetromino) -> bool:
        x_pivot_in_tetromino = tetromino.pivot.x
        y_pivot_in_tetromino = tetromino.pivot.y

        x_pivot_in_grid = tetromino.pivot_in_grid.x
        y_pivot_in_grid = tetromino.pivot_in_grid.y

        rows = len(tetromino.shape)
        cols = len(tetromino.shape[0])

        for i in range(rows):
            for j in range(cols):
                x = x_pivot_in_grid + (j - x_pivot_in_tetromino)
                if x < 0 or x >= GRID_WIDTH:
                    return False

                y = y_pivot_in_grid + (i - y_pivot_in_tetromino)
                if y < 0:
                    return False

                if tetromino.shape[i][j] == BLACK:
                    continue

                if tuple(self.prev_grid[y][x]) != BLACK:
                    return False

        return True

    def update_grid(self, new_tetromino: Tetromino):
        self.curr_tetromino = new_tetromino

        x_pivot_in_tetromino = self.curr_tetromino.pivot.x
        y_pivot_in_tetromino = self.curr_tetromino.pivot.y

        x_pivot_in_grid = self.curr_tetromino.pivot_in_grid.x
        y_pivot_in_grid = self.curr_tetromino.pivot_in_grid.y

        rows = len(self.curr_tetromino.shape)
        cols = len(self.curr_tetromino.shape[0])

        self.grid = [row[:] for row in self.prev_grid]
        for i in range(rows):
            for j in range(cols):
                x = x_pivot_in_grid + (i - x_pivot_in_tetromino)
                y = y_pivot_in_grid + (j - y_pivot_in_tetromino)

                self.grid[x][y] = self.curr_tetromino.shape[i][j]

    def rotate(self):
        new_tetromino = Tetromino(self.curr_tetromino)
        new_tetromino.rotate(1)
        self.change_curr_tetromino(new_tetromino)

    def move_to_left(self):
        new_tetromino = Tetromino(self.curr_tetromino)
        new_tetromino.move_to_left()
        self.change_curr_tetromino(new_tetromino)

    def move_to_right(self):
        new_tetromino = Tetromino(self.curr_tetromino)
        new_tetromino.move_to_right()
        self.change_curr_tetromino(new_tetromino)

    def move_down(self):
        new_tetromino = Tetromino(self.curr_tetromino)
        new_tetromino.move_down()
        if not self.change_curr_tetromino(new_tetromino):
            self.verify_clears()
            self.prev_grid = [row[:] for row in self.grid]
            self.spawn_tetromino()

    def verify_clears(self):
        full_lines = self.get_full_lines()
        removed_lines = 0
        for row in full_lines:
            row = row - removed_lines

            self.grid.pop(row)
            self.grid.insert(0, [BLACK] * 10)

            removed_lines += 1


    def get_full_lines(self):
        y_pivot_in_grid = self.curr_tetromino.pivot_in_grid.y
        y_pivot_in_shape = self.curr_tetromino.pivot.y
        rows_shape = len(self.curr_tetromino.shape)

        start_row = y_pivot_in_grid - y_pivot_in_shape
        end_row = y_pivot_in_grid + (rows_shape -  y_pivot_in_shape)

        full_lines = []
        for i in range(start_row, end_row + 1):
            full_line = True
            for j in range(GRID_WIDTH):
                if tuple(self.grid[i][j]) == BLACK:
                    full_line = False
                    break

            if full_line:
                full_lines.append(i)

        return full_lines

