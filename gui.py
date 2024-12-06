import pygame
from position import Position
from typing import Tuple


def draw_button(window: pygame.Surface, width: int, height: int,
                position: Position, bg_color: Tuple[int, int, int],
                text: str, text_color: Tuple[int, int, int], font: pygame.font.Font
                ):
    pygame.draw.rect(window, bg_color, (position.x, position.y , width, height))

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center = (position.x + width // 2,
                                                position.y + height // 2))

    window.blit(text_surface, text_rect)