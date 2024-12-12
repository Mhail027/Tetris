import numpy as np
from typing import List, Tuple
from constants import *
from engine import *
from position import Position

class Board(Object):
	height: int = GRID_HEIGHT
	width: int = GRID_WIDTH
	grid: list[list[str,...],...] 
	cleared_lines: int = 0	
	
	is_full: bool = False
	cell_scale: float = 1
	cell_size: float = 32

	empty_line: list[str]

	def __init__(self, x: float, y: float, depth: int = 0):
		super().__init__(x, y, depth)
		self.clear()

	def clear(self):
		self.grid = []
		self.empty_line = []
		for i in range(self.width):
			self.empty_line.append('black')
		for j in range(self.height):
			self.grid.append(self.empty_line.copy())

	def verify_space(self, pivot: Position, space: List[List[int]]):
		for j in range(len(space)):
			for i in range(len(space[j])):
				if space[j][i] == 0:
					continue
				if not point_in_rectangle(pivot.x + i, pivot.y + j, 0, 0, self.width - 1, self.height - 1):
					return False
				if (self.grid[pivot.y + j][pivot.x + i] != 'black'):
					return False
		return True
	
	def clear_lines(self):
		idx = self.height - 1
		cleared_lines = 0
		while idx >= 0:
			can_clear = True
			for i in range(self.width):
				if self.grid[idx][i] == 'black':
					can_clear = False
					break
			if can_clear:
				cleared_lines += 1 
				self.grid.pop(idx)
				self.grid.insert(0, self.empty_line.copy())
				idx += 1
			idx -= 1
		self.cleared_lines += cleared_lines
		return cleared_lines

	def merge_tetromino(self, pivot: Position, space: List[List[int]], color: str):
		for j in range(len(space)):
			for i in range(len(space[j])):
				if (space[j][i] != 0):
					self.grid[pivot.y + j][pivot.x + i] = color
		if pivot.y == 0:
			self.is_full = True
			return

	def step_begin(self):
		cell_width = window_get_width() / (self.width + 1)
		cell_height = window_get_height() / (self.height + 1)
		self.cell_scale = min(cell_width / 32, cell_height / 32)
		self.cell_size = self.cell_scale * 32

		board_width = self.cell_size * self.width - self.width
		board_height = self.cell_size * self.height - self.height

		self.x = window_get_width() / 2 - board_width / 2
		self.y = window_get_height() / 2 - board_height / 2

	def draw(self):
		for i in range(self.width):
			for j in range(self.height):
				draw_sprite_ext(self.x + self.cell_size * i - i, self.y + self.cell_size * j - j, 'block_' + self.grid[j][i], 0, self.cell_scale, self.cell_scale)
	
	def draw_end(self):
		draw_set_color((128, 128, 128))
		draw_rectangle(self.x, self.y, self.width * self.cell_size - self.width, self.height * self.cell_size - self.height, True)
