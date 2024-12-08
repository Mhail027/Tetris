import pygame
import numpy
import os
import sys

from constants import *
from enum import Enum

from objectt import *
from sprite import *

pygame.init()

sprites = {}

instances = []

mouse_pressed = {}
mouse_held = {}
mouse_released = {}

keyboard_pressed = {}
keyboard_held = {}
keyboard_released = {}

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
		mouse_pressed.clear()
		mouse_released.clear()
		keyboard_pressed.clear()
		keyboard_released.clear()
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pressed[event.button] = True
				mouse_held[event.button] = True
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_released[event.button] = True
				mouse_held.pop(event.button)
			if event.type == pygame.KEYDOWN:
				keyboard_pressed[event.key] = True
				keyboard_held[event.key] = True
			if event.type == pygame.KEYUP:
				keyboard_released[event.key] = True
				keyboard_held.pop(event.key)
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

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

def sprite_load_all():
	files = os.listdir('./assets/sprites')
	for file in files:
		file_name = os.path.basename(file)
		file_split = os.path.splitext(file_name)
		if file_split[1] == '.png':
			sprite_load('./assets/sprites/' + file)

sprite_load_all()

def mouse_button_check(button):
	if button in mouse_held:
		return True
	return False

def mouse_button_released(button):
	if button in mouse_released:
		return True
	return False

def mouse_button_check_pressed(button):
	if button in mouse_pressed:
		return True
	return False

def keyboard_key_check(key):
	if key in keyboard_held:
		return True
	return False

def keyboard_key_check_pressed(key):
	if key in keyboard_pressed:
		return True
	return False

def keyboard_key_released(key):
	if key in keyboard_released:
		return True
	return False

def level_load(level):
	instances.clear()
	level()

def instance_create(obj: Object):
	for i in range(len(instances)):
		if (instances[i].depth > obj.depth):
			instances.insert(i, obj)
			return obj
	instances.append(obj)
	return obj

def instance_create_depth(x: float, y: float, depth: int, object_name):
	obj = object_name(x, y, depth)
	if not isinstance(obj, Object):
		print("Class used for instancing should be a descendant of Object!!")
		return None
	
	for i in range(len(instances)):
		if (instances[i].depth > obj.depth):
			instances.insert(i, obj)
			return obj
	instances.append(obj)
	return obj

def instance_destroy(obj: Object):
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

def draw_set_font_valign(valign):
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

def draw_set_font_halign(halign):
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

def draw_set_font_align(halign, valign):
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

def draw_set_color(color: tuple[int, int, int]):
	engine.color = color

def draw_set_bgcolor(color: tuple[int, int, int]):
	engine.background_color = color

def draw_clear():
	engine.window.fill(engine.background_color)

def draw_clear_color(color: tuple[int, int, int]):
	engine.window.fill(color)

def point_in_rectangle(x: float, y: float, x1: float, y1: float, x2: float, y2: float):
	if x >= x1 and x <= x2 and y >= y1 and y <= y2:
		return True
	return False

def sprite_get_texture(sprite_name: str):
	return sprites[sprite_name]

# Good solution for circular imports xd
from levels import *
