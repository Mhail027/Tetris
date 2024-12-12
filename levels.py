from engine import instance_create
from menu_handler import MenuHandler
from coop_handler import CoopHandler
from gui import BackButton

def level_main_menu():
	menu_handler = instance_create(MenuHandler(0, 0, 0, 'main_menu'))

def level_play_menu():
	menu_handler = instance_create(MenuHandler(0, 0, 0, 'play_menu'))

def level_coop_menu():
	coop_handler = instance_create(CoopHandler(0, 0, 0))
	back_button = instance_create(BackButton(0, 0, -1))
	back_button.width = 150
	back_button.height = 50
	back_button.relative_x = 0.01
	back_button.relative_y = 0.99
	back_button.relative_corner = ('bottom', 'left')
