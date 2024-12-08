import pygame
import sys

from position import Position

from engine import *
from gui import *

from levels import *

level_load(level_main_menu)

while 1:
    engine.update()
    pygame.display.flip()


