import pygame
from OpenGL.GL import *

#https://learnopengl.com/Getting-started/Camera
cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1,-1))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
side_color = ((1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1))

def solidCube():
    glBegin(GL_QUADS)
    for color, cubeQuad in zip(side_color, cubeQuads):
        glColor3fv(color)
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

# Statup runs once at the start of the game
def startup():
    # enable depth test
    glEnable(GL_DEPTH_TEST)
    # enable smooth shading
    glShadeModel(GL_SMOOTH)

# Pre update runs before event handling and update
def pre_update():
    pass

# Update runs after event handling
# Takes delta time since last frame as argument
def update(delta_time):
    pass

# Event handling
def handle_event(event):
    pass

# Draw runs after updates
def draw():
    solidCube()
    pass

# Cleanup runs once at the end of the game
def cleanup():
    pass