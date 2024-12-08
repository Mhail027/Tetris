from engine import instance_create
from menu_handler import MenuHandler

def level_main_menu():
	menu_handler = instance_create(MenuHandler(0, 0, 0, 'main_menu'))

def level_play_menu():
	menu_handler = instance_create(MenuHandler(0, 0, 0, 'play_menu'))
