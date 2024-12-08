import pygame

from engine import *

class Button(Object):
	width: int
	height: int

	text: str

	selected: bool

	# Leave -1 if position is absolute
	relative_x: float
	relative_y: float

	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)

	def fit_to_text(self):
		pass
	
	def fit_to_window(self):
		pass

	def action(self):
		print('default action')

	def draw(self):
		draw_set_color(WHITE)
		draw_rectangle(self.x, self.y, self.width, self.height, False)		
		
		if self.selected:
			draw_set_color(BLUE)
		else:
			draw_set_color(BLACK)

		draw_rectangle(self.x, self.y, self.width, self.height, True)		
		draw_set_font_align(FontAlignment.CENTER, FontAlignment.MIDDLE)
		draw_set_color(BLACK)
		draw_text(self.x + self.width / 2, self.y + self.y / 2, self.text)
	
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


class PlayButton(Button):
	text = 'Play'
	width = 300
	height = 100

	def __init__(self, x: float, y: float, depth: int = -1):
		super().__init__(x, y, depth)
	
	def action(self):
		print('salut')
