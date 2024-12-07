import pygame

class Sprite:
	texture = None
	origin_x: int
	origin_y: int

	def __init__(self, texture_path: str, x: int, y: int):
		self.texture = pygame.image.load(texture_path).convert_alpha()
		self.origin_x = x
		self.origin_y = y
	
