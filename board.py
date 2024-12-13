import numpy as np
from typing import List, Tuple
from object import Object
from engine import *
from position import Position

class Board(Object):
	height: int = GRID_HEIGHT
	width: int = GRID_WIDTH
	alignment: str
	grid: list[list[str,...],...] 
	cleared_lines: int = 0	
	
	is_full: bool = False
	cell_scale: float = 1
	cell_size: float = 32

	surface = None

	empty_line: list[str]

	def __init__(self, x: float, y: float, depth: int = 0, alignment: str = "CENTER"):
		super().__init__(x, y, depth)
		self.alignment = alignment
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
		if cleared_lines > 0:
			self.update_surface()
		return cleared_lines

	def merge_tetromino(self, pivot: Position, space: List[List[int]], color: str):
		for j in range(len(space)):
			for i in range(len(space[j])):
				if (space[j][i] != 0):
					self.grid[pivot.y + j][pivot.x + i] = color
		if pivot.y == 0:
			first_line_empty = True
			for space in space[0]:
				if space != 'black':
					first_line_empty = False
			if not first_line_empty:
				self.is_full = True
		self.update_surface()

	def step_begin(self):
		if self.alignment == "CENTER":
			self.step_begin_center()
		elif self.alignment == "LEFT":
			self.step_begin_center()
			self.x = 0 + 220
		elif self.alignment == "RIGHT":
			self.step_begin_center()
			self.x = window_get_width() - self.width - self.cell_size * self.width - 220

	def step_begin_center(self):
		cell_width = window_get_width() / (self.width + 1)
		cell_height = window_get_height() / (self.height + 1)
		self.cell_scale = min(cell_width / 32, cell_height / 32)
		self.cell_size = self.cell_scale * 32

		board_width = self.cell_size * self.width - self.width
		board_height = self.cell_size * self.height - self.height

		self.x = window_get_width() / 2 - board_width / 2
		self.y = window_get_height() / 2 - board_height / 2
		if self.surface == None:
			self.surface = surface_create(np.ceil(board_width), np.ceil(board_height))
			self.update_surface()
		if self.surface.get_size() != (np.ceil(board_width), np.ceil(board_height)):
			self.surface = surface_create(np.ceil(board_width), np.ceil(board_height))
			self.update_surface()
		
	def update_surface(self):
		surface_set_target(self.surface)
		for i in range(self.width):
			for j in range(self.height):
				draw_sprite_ext(0 + self.cell_size * i - i, 0 + self.cell_size * j - j, 'block_' + self.grid[j][i], 0, self.cell_scale, self.cell_scale)

		draw_set_color((128, 128, 128))
		draw_rectangle(0, 0, 0 + self.width * self.cell_size - self.width, 0 + self.height * self.cell_size - self.height, True)
		surface_reset_target()

	def draw(self):
		draw_surface(self.x, self.y, self.surface)
	
		
