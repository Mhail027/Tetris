import random

from pygame.examples.midi import null_key

from engine import *
from board import Board
from gui import BackButton
from tetromino import Tetromino
from position import Position

import random

class DuelHandler(Object):
	mode: str = 'local'
	player1: str = 'player1'
	player2: str = 'player2'
	p1_game_board: Board
	p2_game_board: Board
	game_over: bool = False
	p1_next_tetro: str = ''
	p2_next_tetro: str = ''
	tetro_timer = timer_create()
	fall_time = 1.0

	input_delay_time = 0.1
	input1_delay_timer = timer_create()
	input1_delay = False

	input2_delay_timer = timer_create()
	input2_delay = False

	def __init__(self, x: float, y: float, depth: int = 0):
		super().__init__(x, y, depth)

		self.p1_game_board = instance_create_depth(0, 0, 1, Board)
		self.p1_game_board.alignment = "CENTER_LEFT"
		self.p1_game_board.width = 7
		self.p1_game_board.height = 15
		self.p1_game_board.clear()

		self.p2_game_board = instance_create_depth(0, 0, 1, Board)
		self.p2_game_board.alignment = "CENTER_RIGHT"
		self.p2_game_board.width = 7
		self.p2_game_board.height = 15
		self.p2_game_board.clear()

		self.p1_next_tetro = random.choice(TYPES)
		self.p2_next_tetro = random.choice(TYPES)

	def spawn_tetromino(self, owner):
		if owner == self.player1:
			board = self.p1_game_board
			new_tetromino = self.p1_next_tetro
			self.p1_next_tetro = random.choice(TYPES)
		else:
			board = self.p2_game_board
			new_tetromino = self.p2_next_tetro
			self.p2_next_tetro = random.choice(TYPES)

		tw = len(SHAPES[new_tetromino][0])
		tx = (board.width - tw) // 2
		ty = -1 if new_tetromino == 'I' else 0

		tetro = instance_create(Tetromino(tx, ty, 0, new_tetromino))
		tetro.pivot = Position(tx, ty)
		tetro.board = board
		tetro.owner = owner
		return tetro

	def compute_fall_time(self, game_board: Board):
		return max(0.1, self.fall_time - 0.01666 * game_board.cleared_lines)

	def step_begin(self):
		if self.player1 == self.player2:
			self.player2 += '0'
		if self.game_over:
			return

		tetros = instance_get(Tetromino)
		p1tetro = None
		p2tetro = None

		for tetro in tetros:
			if tetro.owner == self.player1:
				p1tetro = tetro
			if tetro.owner == self.player2:
				p2tetro = tetro

		if p1tetro is None:
			self.spawn_tetromino(self.player1)
			timer_start(self.tetro_timer, self.compute_fall_time(self.p1_game_board))

		if p2tetro is None:
			self.spawn_tetromino(self.player2)
			timer_start(self.tetro_timer, self.compute_fall_time(self.p2_game_board))

	def step(self):
		active_tetros = instance_get(Tetromino)
		p1_tetro, p2_tetro = None, None
		for tetro in active_tetros:
			if tetro.owner == self.player1:
				p1_tetro = tetro
			elif tetro.owner == self.player2:
				p2_tetro = tetro

		if not self.input1_delay:
			if p1_tetro is not None:
				if keyboard_key_check(pygame.K_a):
					p1_tetro.move_left(False)
					self.input1_delay = True
				if keyboard_key_check(pygame.K_d):
					p1_tetro.move_right(False)
					self.input1_delay = True
				if keyboard_key_check_pressed(pygame.K_w):
					p1_tetro.rotate(False)
					self.input1_delay = True
				if keyboard_key_check(pygame.K_s):
					p1_tetro.move_down(False)
					self.input1_delay = True
			if self.input1_delay:
				timer_start(self.input1_delay_timer, self.input_delay_time)

		if not self.input2_delay:
			if p2_tetro is not None:
				if keyboard_key_check(pygame.K_LEFT):
					p2_tetro.move_left(False)
					self.input2_delay = True
				if keyboard_key_check(pygame.K_RIGHT):
					p2_tetro.move_right(False)
					self.input2_delay = True
				if keyboard_key_check_pressed(pygame.K_UP):
					p2_tetro.rotate(False)
					self.input2_delay = True
				if keyboard_key_check(pygame.K_DOWN):
					p2_tetro.move_down(False)
					self.input2_delay = True
			if self.input2_delay:
				timer_start(self.input2_delay_timer, self.input_delay_time)

		if self.input1_delay and timer_check(self.input1_delay_timer):
			self.input1_delay = False

		if self.input2_delay and timer_check(self.input2_delay_timer):
			self.input2_delay = False

		if timer_check(self.tetro_timer):
			for tetro, board in [(p1_tetro, self.p1_game_board), (p2_tetro, self.p2_game_board)]:
				if tetro:
					new_pivot = Position(tetro.pivot.x, tetro.pivot.y + 1)
					if not board.verify_space(new_pivot, tetro.shape):
						board.merge_tetromino(tetro.pivot, tetro.shape, tetro.color)
						instance_destroy(tetro)
					else:
						tetro.move_down_forced()
					timer_start(self.tetro_timer, self.compute_fall_time(board))

		for board in [self.p1_game_board, self.p2_game_board]:
			cleared_lines = board.clear_lines()
			if cleared_lines > 0:
				if board == self.p1_game_board:
					self.send_garbage(self.p2_game_board, cleared_lines - 1, self.get_p2_tetro())
				else:
					self.send_garbage(self.p1_game_board, cleared_lines - 1, self.get_p1_tetro())


		if any(board.is_full for board in [self.p1_game_board, self.p2_game_board]):
			self.game_over = True
			for tetro in instance_get(Tetromino):
				instance_destroy(tetro)
			for back_button in instance_get(BackButton):
				back_button.relative_x = -1
				if self.p1_game_board.is_full & self.p2_game_board.is_full:
					back_button.relative_x = 0.5
					back_button.relative_corner = ('bottom', 'center')
				elif self.p2_game_board:
					back_button.x = self.p1_game_board.x + 1.5 * self.p1_game_board.cell_size
				else:
					back_button.x = self.p2_game_board.x + 1.5 * self.p2_game_board.cell_size

				back_button.relative_y = 0.8
				back_button.width = self.p1_game_board.cell_size * 4
				back_button.height = 100


	def draw(self):
		if self.game_over:
			draw_set_alpha(0.8)
			draw_set_color(LTGRAY)
			ww = self.p1_game_board.width * self.p1_game_board.cell_size - self.p1_game_board.width
			hh = self.p1_game_board.height * self.p1_game_board.cell_size - self.p1_game_board.height
			draw_rectangle(self.p1_game_board.x, self.p1_game_board.y, self.p1_game_board.x + ww, self.p1_game_board.y + hh, False)
			draw_rectangle(self.p2_game_board.x, self.p2_game_board.y, self.p2_game_board.x + ww, self.p2_game_board.y + hh, False)

			if not(self.p1_game_board.is_full & self.p2_game_board.is_full):
				draw_set_alpha(1)
				draw_set_color(GREEN)
				tw = text_get_width('WINNER')
				th = text_get_height('WINNER')
				tscale = ww / (tw + 1)
				draw_set_font_halign(FontAlignment.CENTER)
				if self.p2_game_board.is_full:
					draw_text_scaled(self.p1_game_board.x + ww / 2, self.p1_game_board.y + 16 + th * tscale / 2, 'WINNER', tscale, tscale)
				else:
					draw_text_scaled(self.p2_game_board.x + ww / 2, self.p2_game_board.y + 16 + th * tscale / 2, 'WINNER', tscale, tscale)
			else:
				draw_set_alpha(1)
				draw_set_color(GRAY)
				tw = text_get_width('DRAW')
				th = text_get_height('DRAW')
				tscale = ww / (tw + 1)
				draw_set_font_halign(FontAlignment.CENTER)
				draw_text_scaled(self.p1_game_board.x + ww / 2, self.p1_game_board.y + 16 + th * tscale / 2, 'DRAW', tscale, tscale)
				draw_text_scaled(self.p2_game_board.x + ww / 2, self.p2_game_board.y + 16 + th * tscale / 2, 'DRAW', tscale, tscale)




	def draw_end(self):
		if self.game_over:
			return

		draw_set_color(WHITE)

		draw_text(90, 48, 'Next piece for')
		draw_text(58, 78, self.player1 + ':')

		draw_text(window_get_width() - 125, 48, 'Next piece for')
		draw_text(window_get_width() - 157, 78, self.player2 + ':')

		next_tetro_shape = SHAPES[self.p2_next_tetro]
		for j in range(len(next_tetro_shape)):
			for i in range(len(next_tetro_shape[j])):
				if next_tetro_shape[j][i] == 0:
					continue;
				tlen = len(next_tetro_shape[j]) - 1
				xx = window_get_width() - 16 - (tlen - i + 1) * self.p2_game_board.cell_size - tlen - i + 1
				yy = text_get_height('Next piece for' + self.player2 + ':') + 16 + j * self.p2_game_board.cell_size - j
				next_tetro_sprite = 'block_' + SHAPE_COLOR_STR[self.p2_next_tetro]
				draw_sprite_ext(xx, yy + 72, next_tetro_sprite, 0, self.p2_game_board.cell_scale, self.p2_game_board.cell_scale)

		next_tetro_shape = SHAPES[self.p1_next_tetro]
		for j in range(len(next_tetro_shape)):
			for i in range(len(next_tetro_shape[j])):
				if next_tetro_shape[j][i] == 0:
					continue;
				next_tetro_sprite = 'block_' + SHAPE_COLOR_STR[self.p1_next_tetro]
				xx = 16 + i * self.p1_game_board.cell_size - i
				yy = text_get_height('Next peice for ' + self.player1 + ':') + 16 + j * self.p1_game_board.cell_size - j
				draw_sprite_ext(xx, yy + 72, next_tetro_sprite, 0, self.p1_game_board.cell_scale, self.p1_game_board.cell_scale)

	def draw_next_piece(self, tetro_type, x, y):
		next_tetro_shape = SHAPES[tetro_type]
		for j, row in enumerate(next_tetro_shape):
			for i, cell in enumerate(row):
				if cell:
					next_tetro_sprite = 'block_' + SHAPE_COLOR_STR[tetro_type]
					xx = x + i * self.p1_game_board.cell_size
					yy = y + j * self.p1_game_board.cell_size
					draw_sprite_ext(xx, yy, next_tetro_sprite, 0, self.p1_game_board.cell_scale, self.p1_game_board.cell_scale)

	def send_garbage(self, recipient_board: Board, num_lines: int, curr_tetro: Tetromino):
		if num_lines == 0:
			return

		garbage_lines = []
		for _ in range(num_lines):
			garbage_row = ['gray'] * recipient_board.width
			empty_cell = random.randint(0, recipient_board.width - 1)
			garbage_row[empty_cell] = 'black'
			garbage_lines.append(garbage_row)

		recipient_board.grid = recipient_board.grid[num_lines:recipient_board.height] + garbage_lines
		if curr_tetro != null_key:
			while not recipient_board.verify_space(curr_tetro.pivot, curr_tetro.shape):
				curr_tetro.pivot.y -= 1
				if curr_tetro.pivot.y < 0:
					break
		recipient_board.update_surface()

		if not all(cell == 'black' for cell in recipient_board.grid[0]):
			recipient_board.is_full = True

	def get_p1_tetro(self):
		active_tetros = instance_get(Tetromino)
		for tetro in active_tetros:
			if tetro.owner == self.player1:
				return tetro
		return null_key

	def get_p2_tetro(self):
		active_tetros = instance_get(Tetromino)
		for tetro in active_tetros:
			if tetro.owner == self.player2:
				return tetro
		return null_key