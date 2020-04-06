# Copyright (c) 2020 Jhonatan Da Ponte Lopes
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
import pygame
from pygame.locals import QUIT

from keypad import Keypad


display_surf = pygame.display.set_mode((500,500))
pygame.display.set_caption('Button test')

settings1 = {
                "font": pygame.font.SysFont("Segoeuil.ttf", 30),
                "font_color": (0, 0, 0),
                "clicked_color": (130, 130, 130),
                "hover_color": (213, 213, 213),
                "clicked_font_color": (0, 0, 0),
                "hover_font_color": (0, 0, 0)
                }

keypad1 = Keypad((10, 10, 480, 480), gap_size=2, **settings1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keypad1.check_event(event)
    
    display_surf.fill((230, 230, 230))
    keypad1.draw(display_surf)
    pygame.display.update()