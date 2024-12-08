import pygame

from engine import *

class Button(Object):
	width = 60
	height = 60
	sprite_name = 'kid'
	angle = 0
	def __init__(self, x: float, y: float, depth: int):
		super().__init__(x, y, depth)

	def action(self):
		pass

	def draw_begin(self):
		draw_line(window_get_width() / 2, 0, window_get_width() / 2, window_get_height())
		draw_line(0, window_get_height() / 2, window_get_width(), window_get_height() / 2)
		draw_sprite_ext(window_get_width() / 2, window_get_height() / 2, self.sprite_name, self.angle, 1, 1)
		self.angle += 1

	def draw_end(self):
		draw_rectangle(self.x, self.y, self.width, self.height, True)
		font_align(FontAlignment.LEFT, FontAlignment.MIDDLE)
		draw_text_scaled(self.x + self.width, self.y + self.height / 2, 'Salutari', 3, 3)
			

