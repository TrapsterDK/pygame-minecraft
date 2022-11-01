import pygame
from gameengine import quit_game

# Event handling
def handle_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            quit_game()