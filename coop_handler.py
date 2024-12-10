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
	score: int = 0
	game_over: bool = False
	next_tetromino: str = ''
	fall_timer = timer_create()
	fall_time = 1

	input_delay_timer = timer_create()
	input_delay_time = 0.1
	input_delay = False

	def __init__(self, x: float, y: float, depth: int = 0):
		super().__init__(x, y, depth)
		self.game_board = instance_create_depth(0, 0, 1, Board)
		self.game_board.width = 10
		self.game_board.height = 20
		self.game_board.clear()
		self.next_tetromino = random.choice(TYPES)

	def spawn_tetromino(self):
		tx = self.game_board.width // 2
		tx -= len(SHAPES[self.next_tetromino][0]) // 2
		ty = 0
		tetro = instance_create(Tetromino(0, 0, 0, self.next_tetromino))
		tetro.pivot = Position(tx, ty)
		tetro.board = self.game_board
		tetro.step()
		self.next_tetromino = random.choice(TYPES)
	
	def step_begin(self):
		if not instance_exists(Tetromino):
			self.spawn_tetromino()
			timer_start(self.fall_timer, self.fall_time - 0.00833 * self.game_board.cleared_lines)
	
	def step(self):
		active_tetro = instance_get(Tetromino)
		if active_tetro != None:
			if not self.input_delay:
				if keyboard_key_check(pygame.K_a):
					active_tetro.move_left()
					self.input_delay = True
					timer_start(self.input_delay_timer, self.input_delay_time)
				if keyboard_key_check(pygame.K_d):
					active_tetro.move_right()
					self.input_delay = True
					timer_start(self.input_delay_timer, self.input_delay_time)
				if keyboard_key_check(pygame.K_s):
					active_tetro.move_down()
					self.input_delay = True
					timer_start(self.fall_timer, self.fall_time - 0.00833 * self.game_board.cleared_lines)
					timer_start(self.input_delay_timer, self.input_delay_time)
				if keyboard_key_check_pressed(pygame.K_w):
					active_tetro.rotate()
					self.input_delay = True
					timer_start(self.input_delay_timer, self.input_delay_time)
			if timer_check(self.fall_timer):
				active_tetro.move_down()
				timer_start(self.fall_timer, self.fall_time - 0.0083 * self.game_board.cleared_lines)
			if timer_check(self.input_delay_timer):
				self.input_delay = False

	def draw(self):
		draw_set_font_align(FontAlignment.LEFT, FontAlignment.TOP)
		draw_set_color(BLACK)
		draw_text(0, 0, str(self.game_board.cleared_lines))
