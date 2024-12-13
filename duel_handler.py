import random
from engine import *
from board import Board
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
		self.p1_game_board.alignment = "LEFT"
		self.p1_game_board.width = 7
		self.p1_game_board.height = 15
		self.p1_game_board.clear()

		self.p2_game_board = instance_create_depth(0, 0, 1, Board)
		self.p2_game_board.alignment = "RIGHT"
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
					self.send_garbage(self.p2_game_board, cleared_lines - 1)
				else:
					self.send_garbage(self.p1_game_board, cleared_lines - 1)


		if any(board.is_full for board in [self.p1_game_board, self.p2_game_board]):
			self.game_over = True


	def draw(self):
		draw_set_color(WHITE)

		draw_text(90, 48, 'Next piece for')
		draw_text(58, 78, self.player1 + ':')

		draw_text(window_get_width() - 125, 48, 'Next piece for')
		draw_text(window_get_width() - 157, 78, self.player2 + ':')

	def draw_end(self):
		if self.game_over:
			return

		self.draw_next_piece(self.p1_next_tetro, 16, 100)
		self.draw_next_piece(self.p2_next_tetro, window_get_width() - 200, 100)

	def draw_next_piece(self, tetro_type, x, y):
		next_tetro_shape = SHAPES[tetro_type]
		for j, row in enumerate(next_tetro_shape):
			for i, cell in enumerate(row):
				if cell:
					next_tetro_sprite = 'block_' + SHAPE_COLOR_STR[tetro_type]
					xx = x + i * self.p1_game_board.cell_size
					yy = y + j * self.p1_game_board.cell_size
					draw_sprite_ext(xx, yy, next_tetro_sprite, 0, self.p1_game_board.cell_scale, self.p1_game_board.cell_scale)

	def send_garbage(self, recipient_board: Board, num_lines: int):
		if num_lines == 0:
			return

		garbage_lines = []
		for _ in range(num_lines):
			garbage_row = ['gray'] * recipient_board.width
			empty_cell = random.randint(0, recipient_board.width - 1)
			garbage_row[empty_cell] = 'black'
			garbage_lines.append(garbage_row)

		if not all(cell == 'black' for cell in recipient_board.grid[num_lines - 1]):
			self.game_over = True
		recipient_board.grid = recipient_board.grid[1:recipient_board.height] + garbage_lines
		recipient_board.update_surface()
