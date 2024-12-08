import pygame
import sys

import levels

from engine import *

class Button(Object):
	width = 0
	height = 0

	text = ''

	selected = False

	# Position relative to the window
	# Leave -1 if position is absolute
	relative_x = -1
	relative_y = -1

	# Leave None if position is absolute or relative to the window
	relative_to = None
	# up, down, left or right
	relative_dir = ('none')
	relative_spacing = 10

	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)

	def fit_to_text(self):
		pass
	
	def fit_to_window(self):
		pass

	def action(self):
		print('default action')

	def draw_background(self):
		draw_set_color(WHITE)
		draw_rectangle(self.x, self.y, self.width, self.height, False)

	def draw_outline(self):
		if self.selected:
			draw_set_color(BLUE)
		else:
			draw_set_color(BLACK)

		draw_rectangle(self.x, self.y, self.width, self.height, True)
	
	def draw_own_text(self):
		draw_set_font_align(FontAlignment.CENTER, FontAlignment.MIDDLE)
		draw_set_color(BLACK)
		draw_text(self.x + self.width / 2, self.y + self.height / 2, self.text)

	def draw(self):
		self.draw_background()
		self.draw_outline()
		self.draw_own_text()	
	
	def step_begin(self):
		if self.relative_x >= 0:
			self.x = window_get_width() * self.relative_x - self.width / 2
		if self.relative_y >= 0:
			self.y = window_get_height() * self.relative_y - self.height / 2
		if self.relative_to != None:
			offx = 0
			offy = 0
			if 'up' in self.relative_dir:
				offy -= self.height + self.relative_spacing
			if 'down' in self.relative_dir:
				offy += self.relative_to.height + self.relative_spacing
			if 'right' in self.relative_dir:
				offx += self.relative_to.width + self.relative_spacing
			if 'left' in self.relative_dir:
				offx -= self.width + self.relative_spacing
			self.x = self.relative_to.x + offx
			self.y = self.relative_to.y + offy

	def step(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		self.selected = False
		if point_in_rectangle(mouse_x, mouse_y, self.x, self.y, self.x + self.width, self.y + self.height):
			self.selected = True
			if mouse_button_check_pressed(MB_LEFT):
				self.action()
		if keyboard_key_check(pygame.K_a):
			self.x -= 1
		if keyboard_key_check(pygame.K_d):
			self.x += 1

class ImageButton(Button):
	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)
	
	def draw_own_text(self):
		draw_set_font_align(FontAlignment.CENTER, FontAlignment.MIDDLE)
		draw_set_color(BLACK)
		th = text_get_height(self.text)
		draw_text(self.x + self.width / 2, self.y + self.height + th + 16, self.text)
	
	def draw_end(self):
		spr = sprite_get_texture(self.sprite_name)
		sw, sh = spr.texture.get_size()
		draw_sprite_ext(self.x, self.y, self.sprite_name, 0, self.width / sw, self.height / sh)

class PlayButton(Button):
	text = 'Play'
	width = 300
	height = 100
	
	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)
	
	def action(self):
		level_load(levels.level_play_menu)

class QuitButton(Button):
	text = 'Quit'
	width = 300
	height = 100

	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)
	
	def action(self):
		pygame.quit()
		sys.exit()

class DuelButton(ImageButton):
	sprite_name = 'duel_button'
	text = 'Duel against your friends'
	width = 200
	height = 200

	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)
	
	def action(self):
		pass

class CoopButton(ImageButton):
	sprite_name = 'coop_button'
	text = 'Cooperate with your friends'
	width = 200
	height = 200

	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)
	
	def action(self):
		pass

class BackButton(Button):
	text = 'Back'
	width = 300
	height = 100

	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)

	def action(self):
		level_load(levels.level_main_menu)

