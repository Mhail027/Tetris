import random
from engine import *
from board import Board
from tetromino import Tetromino
from position import Position

import random

class CoopHandler(Object):
	mode: str = 'local'
	player1: str = 'player1'
	player2: str = 'player2'
	game_board: Board
	score: float = 0
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
		self.game_board = instance_create_depth(0, 0, 1, Board)
		self.game_board.width = 15
		self.game_board.height = 25
		self.game_board.clear()
		self.p1_next_tetro = random.choice(TYPES)
		self.p2_next_tetro = random.choice(TYPES)

	def spawn_tetromino(self, owner):
		new_tetromino = self.p1_next_tetro
		if owner == self.player2:
			new_tetromino = self.p2_next_tetro
		tx = 0
		tw = len(SHAPES[new_tetromino][0])
		if owner == self.player1:
			tx = 1
		if owner == self.player2:
			tx = self.game_board.width - tw - 1
		ty = 0
		if (new_tetromino == 'I'):
			ty = -1
		tetro = instance_create(Tetromino(0, 0, 0, new_tetromino))
		tetro.pivot = Position(tx, ty)
		tetro.board = self.game_board
		tetro.owner = owner
		if owner == self.player1:
			self.p1_next_tetro = random.choice(TYPES)
		else:
			self.p2_next_tetro = random.choice(TYPES)
		return tetro
	
	def compute_fall_time(self):
		return max(0.1, self.fall_time - 0.01666 * self.game_board.cleared_lines)

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
		
		if p1tetro == None:
			self.spawn_tetromino(self.player1)
			timer_start(self.tetro_timer, self.compute_fall_time())

		if p2tetro == None:
			self.spawn_tetromino(self.player2)
			timer_start(self.tetro_timer, self.compute_fall_time())
			


	def step(self):
		active_tetros = instance_get(Tetromino)
		tetro1 = None
		tetro2 = None
		for tetro in active_tetros:
			if tetro.owner == self.player1:
				tetro1 = tetro
			if tetro.owner == self.player2:
				tetro2 = tetro
	
		if not self.input1_delay:	
			if tetro1 != None:	
				if keyboard_key_check(pygame.K_a):
					tetro1.move_left()
					self.input1_delay = True
				if keyboard_key_check(pygame.K_d):
					tetro1.move_right()
					self.input1_delay = True
				if keyboard_key_check_pressed(pygame.K_w):
					tetro1.rotate()
					self.input1_delay = True
				if keyboard_key_check(pygame.K_s):
					tetro1.move_down()
					self.input1_delay = True
					self.score += 0.1
			if self.input1_delay:
				timer_start(self.input1_delay_timer, self.input_delay_time)
		if not self.input2_delay:
			if tetro2 != None:
				if keyboard_key_check(pygame.K_LEFT):
					tetro2.move_left()
					self.input2_delay = True
				if keyboard_key_check(pygame.K_RIGHT):
					tetro2.move_right()
					self.input2_delay = True
				if keyboard_key_check_pressed(pygame.K_UP):
					tetro2.rotate()
					self.input2_delay = True
				if keyboard_key_check(pygame.K_DOWN):
					tetro2.move_down()
					self.input2_delay = True
					self.score += 0.1
			if self.input2_delay:
				timer_start(self.input2_delay_timer, self.input_delay_time)
		
		if self.input1_delay and timer_check(self.input1_delay_timer):
			self.input1_delay = False

		if self.input2_delay and timer_check(self.input2_delay_timer):
			self.input2_delay = False

		if timer_check(self.tetro_timer):
			if tetro1 != None:
				new_pivot = Position(tetro1.pivot.x, tetro1.pivot.y + 1)
				if not self.game_board.verify_space(new_pivot, tetro1.shape):
					self.game_board.merge_tetromino(tetro1.pivot, tetro1.shape, tetro1.color)
					instance_destroy(tetro1)
					tetro1 = None
			if tetro2 != None:
				new_pivot = Position(tetro2.pivot.x, tetro2.pivot.y + 1)
				if not self.game_board.verify_space(new_pivot, tetro2.shape):
					self.game_board.merge_tetromino(tetro2.pivot, tetro2.shape, tetro2.color)
					instance_destroy(tetro2)
					tetro2 = None

			if tetro1 != None:
				tetro1.move_down_forced()
			if tetro2 != None:
				tetro2.move_down_forced()
			timer_start(self.tetro_timer, self.compute_fall_time())
			
		cleared_lines = self.game_board.clear_lines()
		if cleared_lines > 0:
			self.score += cleared_lines * 10 + 5 * (cleared_lines - 1)
		if self.game_over == False and self.game_board.is_full:
			self.game_over = True

	def draw(self):
		draw_set_font_align(FontAlignment.LEFT, FontAlignment.TOP)
		draw_set_color(WHITE)
		draw_text(16, 16, 'Score: ' + str(int(self.score * 10)))
		draw_text(16, 400, 'FPS: ' + str(fps_get()))

	def draw_end(self):
		if self.game_over:
			return

		draw_set_color(WHITE)
		draw_set_font_halign(FontAlignment.RIGHT)
		draw_text(window_get_width() - 16, 48, 'Next piece for ' + self.player2 + ':')
		draw_set_font_halign(FontAlignment.LEFT)
		draw_text(16, 48, 'Next piece for ' + self.player1 + ':')
		
		next_tetro_shape = SHAPES[self.p2_next_tetro]
		for j in range(len(next_tetro_shape)):
			for i in range(len(next_tetro_shape[j])):
				if next_tetro_shape[j][i] == 0:
					continue;
				tlen = len(next_tetro_shape[j]) - 1
				xx = window_get_width() - 16 - (tlen - i + 1) * self.game_board.cell_size - tlen - i + 1
				yy = text_get_height('Next piece for' + self.player2 + ':') + 16 + j * self.game_board.cell_size - j
				next_tetro_sprite = 'block_' + SHAPE_COLOR_STR[self.p2_next_tetro]
				draw_sprite_ext(xx, yy + 32, next_tetro_sprite, 0, self.game_board.cell_scale, self.game_board.cell_scale)

		next_tetro_shape = SHAPES[self.p1_next_tetro]
		for j in range(len(next_tetro_shape)):
			for i in range(len(next_tetro_shape[j])):
				if next_tetro_shape[j][i] == 0:
					continue;
				next_tetro_sprite = 'block_' + SHAPE_COLOR_STR[self.p1_next_tetro]
				xx = 16 + i * self.game_board.cell_size - i
				yy = text_get_height('Next peice for ' + self.player1 + ':') + 16 + j * self.game_board.cell_size - j
				draw_sprite_ext(xx, yy + 32, next_tetro_sprite, 0, self.game_board.cell_scale, self.game_board.cell_scale)
