from engine import *
from gui import *

class MenuHandler(Object):
	menu_state: str

	def __init__(self, x: float, y: float, depth: int, menu_state: str = 'main_menu'):
		super().__init__(x, y, depth)
		self.mane_state = menu_state

		match menu_state:
			case 'main_menu':
				self.create_main_menu()

			case 'play_menu':
				self.create_play_menu()

			case _:
				self.create_main_menu()
	
	def create_main_menu(self):
		play_button = instance_create_depth(0, 0, -1, PlayButton)
		play_button.relative_x = 0.5
		play_button.relative_y = 0.4
		play_button.relative_corner = ('center')

		quit_button = instance_create_depth(0, 0, -1, QuitButton)
		quit_button.relative_to = play_button
		quit_button.relative_spacing = 32
		quit_button.relative_dir = ('bottom')
	
	def create_play_menu(self):
		back_button = instance_create_depth(32, 0, -1,BackButton)
		back_button.relative_x = 0.01
		back_button.relative_y = 0.99
		back_button.relative_corner = ('bottom', 'left')

		duel_button = instance_create_depth(0, 0, -1, DuelButton)
		duel_button.relative_x = 0.33
		duel_button.relative_y = 0.3
		duel_button.relative_corner = ('center')

		coop_button = instance_create_depth(0, 0, -1, CoopButton)
		coop_button.relative_x = 0.66
		coop_button.relative_y = 0.3
		coop_button.relative_corner = ('center')
