import pygame
import sys

from position import Position

from engine import *
from gui import *

sprite_load('./assets/sprites/kid.png', 32, 32)

instance_create(Button(100, 100, 60, 60))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    engine.update()
    pygame.display.flip()


