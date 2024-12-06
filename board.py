import numpy as np
from typing import List, Tuple
from constants import *
from tetromino import Tetromino


class Board:
    height: int = GRID_HEIGHT
    width: int = GRID_WIDTH
    grid: List[List[Tuple[int, int, int]]]
    curr_tetromino: Tetromino
    score: int
    game_over: bool

    def __init__(self):
        self.clear()

    def clear(self):
        self.grid = np.full((self.height, self.width),
                            (0, 0, 0),
                            dtype = object).tolist()
        self.score = 0
        self.game_over = False


