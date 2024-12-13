import pygame

class Object:
	x: float
	y: float
	depth: int
	
	sprite_name = ''

	def __init__(self, x: float, y: float, depth: int):
		self.x = x
		self.y = y
		self.depth = depth

	# Event functions:
	def step(self):
		# nothing
		pass
	
	def draw(self):
		self.draw_self()
	
	def step_begin(self):
		#nothing
		pass
	
	def step_end(self):
		#nothing
		pass
	
	def draw_begin(self):
		#nothing
		pass
	
	def draw_end(self):
		#nothing
		pass

	# Basic functions
	# DO NOT OVERRIDE
	def draw_self(self):
		if self.sprite_name != '':
			from engine import draw_sprite
			draw_sprite(self.x, self.y, self.sprite_name)

	def destroy(self):
		from engine import instance_destroy
		instance_destroy(self)

