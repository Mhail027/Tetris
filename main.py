import pygame
import sys

from position import Position

from engine import *
from gui import *

sprite_load('./assets/sprites/kid.png', 32, 32)

button = instance_create_depth(100, 100, -1, PlayButton)

while 1:
    engine.update()
    pygame.display.flip()


