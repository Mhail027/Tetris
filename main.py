import pygame
import sys

from constants import *
from gui import draw_button
from position import Position

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

font = pygame.font.Font(None, 36)
draw_button(window, BUTTON_WIDTH, BUTTON_HEIGHT,
            Position(100, 70), GRAY,
            "Cooperative Mode", BLACK, font)
draw_button(window, BUTTON_WIDTH, BUTTON_HEIGHT,
            Position(100, 230),GRAY,
            "Competitive Mode", BLACK, font)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()


