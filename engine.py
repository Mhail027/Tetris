import pygame
import numpy
import os

from constants import *
from enum import Enum

from object import *
from sprite import *

pygame.init()

sprites = {}

instances = []

class FontAlignment(Enum):
	# Horizontal Alignment
	LEFT = 0
	CENTER = 1
	RIGHT = 2
	# Vertical Alignment
	TOP = 3
	MIDDLE = 4
	BOTTOM = 5

class Engine:
	window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	font = pygame.font.Font(None, 36)
	fa_vertical = FontAlignment.MIDDLE
	fa_horizontal = FontAlignment.CENTER

	color = (0, 0, 0)
	background_color = (255, 255, 255)

	def __init__(self):
		pygame.display.set_caption('Tetris');
		pass
	
	def update(self):
		# Normally, you would want these events to be in a separate for loop,
		# but we ball
		for instance in instances:
			instance.step_begin()
			instance.step()
			instance.step_end()
		self.window.fill((255, 255, 255))
		for instance in instances:
			instance.draw_begin()
			instance.draw()
			instance.draw_end()

engine = Engine()

def sprite_load(sprite_path: str, origin_x: int = 0, origin_y: int = 0):
	file_name = os.path.basename(sprite_path)
	file = os.path.splitext(file_name)
	sprites[file[0]] = Sprite(sprite_path, origin_x, origin_y)

def instance_create(obj: object):
	for i in range(len(instances)):
		if (instances[i].depth > obj.depth):
			instances.insert(i, obj)
			return
	instances.append(obj)

def instance_destroy(obj: object):
	instances.remove(obj)

def window_get_width():
	w, h = pygame.display.get_window_size()
	return w

def window_get_height():
	w, h = pygame.display.get_window_size()
	return h

def draw_line(x1: float, y1: float, x2: float, y2: float, width: int = 2):
	pygame.draw.line(engine.window, engine.color, (x1, y1), (x2, y2), 2)

def draw_rectangle(x: float, y: float, width: float, height: float, outline: bool = False):
	if outline == False:
		pygame.draw.rect(engine.window, engine.color, pygame.Rect(x, y, width, height))
		return
	pygame.draw.line(engine.window, engine.color, (x, y), (x + width, y), 2)
	pygame.draw.line(engine.window, engine.color, (x, y), (x, y + height), 2)
	pygame.draw.line(engine.window, engine.color, (x + width, y), (x + width, y + height), 2)
	pygame.draw.line(engine.window, engine.color, (x, y + height), (x + width, y + height), 2)

def draw_sprite_ext(x: float, y: float, sprite_name: str, angle: float = 0, xscale: float = 1, yscale: float = 1):
	sprite = sprites[sprite_name]
	sw, sh = sprite.texture.get_size()
	scaled_sprite = pygame.transform.scale_by(sprite.texture, (xscale, yscale))
	rotated_sprite = pygame.transform.rotate(scaled_sprite, angle)
	rangle = angle * numpy.pi / 180

	box = [pygame.math.Vector2(p) for p in [(0, 0), (sw, 0), (sw, -sh), (0, -sh)]]
	box_rotate = [p.rotate(angle) for p in box]
	min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
	max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

	rotated_ox = sprite.origin_x * numpy.cos(rangle) + sprite.origin_y * numpy.sin(rangle) 
	rotated_oy = sprite.origin_x * numpy.sin(rangle) - sprite.origin_y * numpy.cos(rangle)
	engine.window.blit(rotated_sprite, (x + min_box[0] - rotated_ox, y - max_box[1] + rotated_oy))

def draw_sprite(x: float, y: float, sprite_name: str):
	sprite = sprites[sprite_name]
	engine.window.blit(sprite.texture, (x - sprite.origin_x, y - sprite.origin_y))

def draw_text(x: float, y: float, text: str):
	text_width, text_height = engine.font.size(text)
	rendered_text = engine.font.render(text, True, engine.color)
	xx = x
	yy = y
	
	match engine.fa_horizontal:
		case FontAlignment.LEFT:
			xx = x
		case FontAlignment.CENTER:
			xx = x - text_width / 2
		case FontAlignment.RIGHT:
			xx = x - text_width
		case _:
			xx = x
	
	match engine.fa_vertical:
		case FontAlignment.TOP:
			yy = y
		case FontAlignment.MIDDLE:
			yy = y - text_height / 2
		case FontAlignment.BOTTOM:
			yy = y - text_height
		case _:
			yy = y
	
	engine.window.blit(rendered_text, (xx, yy))

def draw_text_scaled(x: float, y: float, text: str, xscale: float, yscale: float):
	text_width, text_height = engine.font.size(text)
	rendered_text = engine.font.render(text, True, engine.color)
	rendered_text = pygame.transform.scale_by(rendered_text, (xscale, yscale))
	xx = x
	yy = y
	
	match engine.fa_horizontal:
		case FontAlignment.LEFT:
			xx = x
		case FontAlignment.CENTER:
			xx = x - xscale * text_width / 2
		case FontAlignment.RIGHT:
			xx = x - xscale * text_width
		case _:
			xx = x
	
	match engine.fa_vertical:
		case FontAlignment.TOP:
			yy = y
		case FontAlignment.MIDDLE:
			yy = y - yscale * text_height / 2
		case FontAlignment.BOTTOM:
			yy = y - yscale * text_height
		case _:
			yy = y
	
	engine.window.blit(rendered_text, (xx, yy))

def text_get_width(text: str):
	text_width, text_height = engine.font.size(text)
	return text_width

def text_get_height(text: str):
	text_width, text_height = engine.font.size(text)
	return text_height

def text_get_size(text: str):
	return engine.font.size(text)

def font_valign(valign):
	valid = False
	match valign:
		case FontAlignment.TOP:
			valid = True
		case FontAlignment.MIDDLE:
			valid = True
		case FontAlignment.BOTTOM:
			valid = True
		case _:
			valid = False
	if (valid):
		engine.fa_vertical = valign
	else:
		engine.fa_vertical = FontAlignment.MIDDLE

def font_halign(halign):
	valid = False
	match halign:
		case FontAlignment.LEFT:
			valid = True
		case FontAlignment.CENTER:
			valid = True
		case FontAlignment.RIGHT:
			valid = True
		case _:
			valid = False
	if (valid):
		engine.fa_horizontal = halign
	else:
		engine.fa_horizontal = FontAlignment.CENTER

def font_align(halign, valign):
	valid = False
	match valign:
		case FontAlignment.TOP:
			valid = True
		case FontAlignment.MIDDLE:
			valid = True
		case FontAlignment.BOTTOM:
			valid = True
		case _:
			valid = False
	if (valid):
		engine.fa_vertical = valign
	else:
		engine.fa_vertical = FontAlignment.MIDDLE

	valid = False
	match halign:
		case FontAlignment.LEFT:
			valid = True
		case FontAlignment.CENTER:
			valid = True
		case FontAlignment.RIGHT:
			valid = True
		case _:
			valid = False
	if (valid):
		engine.fa_horizontal = halign
	else:
		engine.fa_horizontal = FontAlignment.CENTER

