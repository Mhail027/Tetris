import random
import numpy as np
from typing import List, Tuple
from constants import *

class Tetromino:
    type: str
    shape: List[List[Tuple[int, int, int]]]
    pivot: Position
    pivot_in_grid: Position

    def __init__(self, tetromino: 'Tetromino' = None):
        if tetromino is None:
            self.type = random.choice(TYPES)
        else:
            self.type = tetromino.type

        self.shape = SHAPES.get(self.type)
        self.pivot = INITIAL_PIVOTS.get(self.type)
        self.pivot_in_grid = Position(5, self.pivot.y)

        if Tetromino is None:
            self.rotate(random.choice([0, 1, 2, 3]))


    # Rotate to right
    def rotate(self, rotations: int):
        rotations = rotations % 4
        for i in range(rotations):
            transposed_matrix = np.transpose(self.shape).tolist()
            self.pivot.flip()

            self.shape = np.flip(transposed_matrix).tolist()
            self.pivot.y = len(self.shape[0]) - self.pivot.y

    def move_to_left(self):
        self.pivot_in_grid.x -= 1

    def move_to_right(self):
        self.pivot_in_grid.x += 1

    def move_down(self):
        self.pivot_in_grid.y += 1

