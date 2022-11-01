import pygame

# Statup runs once at the start of the game
def startup():
    pass

# Pre update runs before event handling and update
def pre_update():
    pass

# Update runs after event handling, return true to redraw the screen
# Takes delta time since last frame as argument
def update(delta_time):
    return True

# Event handling, return true to close the game
def handle_event(event):
    return False

# Draw runs after update if update or pre update returned true
def draw():
    pass

# Cleanup runs once at the end of the game
def cleanup():
    pass