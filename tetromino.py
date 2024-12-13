import random
import numpy as np
from typing import List, Tuple
from constants import *
from engine import *
from position import Position
from board import Board

class Tetromino(Object):
	type: str
	shape: List[List[int]]

	color: str
	pivot: Position
	board: Board
	owner: str

	def __init__(self, x: float, y: float, depth: int = 0, shape: str = 'O'):
		super().__init__(x, y, depth)
		self.type = shape
		self.shape = SHAPES.get(self.type)
		self.color = SHAPE_COLOR_STR.get(self.type)
		self.sprite_name = 'block_' + self.color
	
	# Rotate to right
	def rotate(self, verify_collision: bool = True):
		old_shape = self.shape
		transposed_matrix = np.transpose(self.shape).tolist()
		rotated_matrix_cc = np.fliplr(transposed_matrix).tolist()
		self.shape = rotated_matrix_cc
		new_pivot = Position(self.pivot.x, self.pivot.y)
		if new_pivot.x < 0:
			ignore = True
			for i in range(len(self.shape)):
				if self.shape[i][0] != 0:
					ignore = False
					break
			if not ignore:
				new_pivot.x = 0
		if new_pivot.x > self.board.width - len(self.shape[0]):
			ignore = True
			for i in range(len(self.shape)):
				if self.shape[i][len(self.shape[0]) - 1] != 0:
					ignore = False
					break
			if not ignore:
				new_pivot.x = self.board.width - len(self.shape[0])
		if new_pivot.y < 0:
			ignore = True
			for i in range(len(self.shape[0])):
				if self.shape[0][i] != 0:
					ignore = False
					break
			if not ignore:
				new_pivot.y = 0
		if new_pivot.y > self.board.height - len(self.shape):
			ignore = True
			for i in range(len(self.shape[0])):
				if self.shape[len(self.shape) - 1][i] != 0:
					ignore = False
					break
			if not ignore:
				new_pivot.y = self.board.height - len(self.shape)


		if verify_collision & self.check_tetro_collision(new_pivot):
			self.shape = old_shape
			return
		
		if self.board.verify_space(new_pivot, rotated_matrix_cc):
			self.shape = rotated_matrix_cc
			self.pivot = new_pivot
			return
		self.shape = old_shape
	
	def check_tetro_collision(self, pivot: Position):
		for tetro in instance_get(Tetromino):
			if tetro == self:
				continue
			for sy in range(len(self.shape)):
				for sx in range(len(self.shape[0])):
					for ty in range(len(tetro.shape)):
						for tx in range(len(tetro.shape[0])):
							if self.shape[sy][sx] == 0 or tetro.shape[ty][tx] == 0:
								continue
							if pivot.x + sx == tetro.pivot.x + tx and pivot.y + sy == tetro.pivot.y + ty:
								return True
		return False
	
	def move_left(self, verify_collision: bool = True):
		new_pivot = Position(self.pivot.x - 1, self.pivot.y)
		if verify_collision & self.check_tetro_collision(new_pivot):
			return
		if self.board.verify_space(new_pivot, self.shape):
			self.pivot = new_pivot

	def move_right(self, verify_collision: bool = True):
		new_pivot = Position(self.pivot.x + 1, self.pivot.y)
		if verify_collision & self.check_tetro_collision(new_pivot):
			return
		if self.board.verify_space(new_pivot, self.shape):
			self.pivot = new_pivot

	def move_down(self, verify_collision: bool = True):
		new_pivot = Position(self.pivot.x, self.pivot.y + 1)
		if verify_collision & self.check_tetro_collision(new_pivot):
			return
		if self.board.verify_space(new_pivot, self.shape):
			self.pivot = new_pivot

	def move_down_forced(self):
		new_pivot = Position(self.pivot.x, self.pivot.y + 1)
		if self.board.verify_space(new_pivot, self.shape):
			self.pivot = new_pivot
		else:
			self.board.merge_tetromino(self.pivot, self.shape, self.color)
			instance_destroy(self)

	def step(self):
		self.x = self.board.x + self.pivot.x * self.board.cell_size - self.pivot.x
		self.y = self.board.y + self.pivot.y * self.board.cell_size - self.pivot.y

	def draw(self):
		for j in range(len(self.shape)):
			for i in range(len(self.shape[j])):
				if self.shape[j][i] == 0:
					continue
				xx = self.x + i * self.board.cell_size - i
				yy = self.y + j * self.board.cell_size - j
				draw_sprite_ext(xx, yy, self.sprite_name, 0, self.board.cell_scale, self.board.cell_scale)
