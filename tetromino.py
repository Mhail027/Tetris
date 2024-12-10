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

	def __init__(self, x: float, y: float, depth: int = 0, shape: str = 'O'):
		super().__init__(x, y, depth)
		self.type = shape
		self.shape = SHAPES.get(self.type)
		self.color = SHAPE_COLOR_STR.get(self.type)
		self.sprite_name = 'block_' + self.color
	
	# Rotate to right
	def rotate(self):
		transposed_matrix = np.transpose(self.shape).tolist()
		rotated_matrix_cc = np.fliplr(transposed_matrix).tolist()
		rotated_matrix_cw = np.flipud(transposed_matrix).tolist()
		if self.board.verify_space(self.pivot, rotated_matrix_cc):
			self.shape = rotated_matrix_cc
		elif self.board.verify_space(self.pivot, rotated_matrix_cw):
			self.shape = rotated_matrix_cw
			

	def move_left(self):
		new_pivot = Position(self.pivot.x - 1, self.pivot.y)
		if self.board.verify_space(new_pivot, self.shape):
			self.pivot = new_pivot

	def move_right(self):
		new_pivot = Position(self.pivot.x + 1, self.pivot.y)
		if self.board.verify_space(new_pivot, self.shape):
			self.pivot = new_pivot

	def move_down(self):
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
