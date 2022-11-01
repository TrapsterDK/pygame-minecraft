import pygame
from OpenGL.GL import *

cube_vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

cube_edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

cube_quads = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

side_color = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1)
)

uv_coords = (
    (0, 0),
    (0, 1),
    (1, 1),
    (1, 0)
)

def cube():
    glBegin(GL_QUADS)
    glColor3f(0, 0, 0)
    for cube_quad in cube_quads:
        for vertex in cube_quad:
            glVertex3fv(cube_vertices[vertex])
    glEnd()

def colored_cube():
    glBegin(GL_QUADS)
    for i in range(6):
        glColor3fv(side_color[i])
        for vertex in cube_quads[i]:
            glVertex3fv(cube_vertices[vertex])
    glEnd()

def grid_cube():
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv(cube_vertices[vertex])
    glEnd()

cube_display = 0
cube_drawing_functions = [colored_cube, grid_cube, cube]

# Statup runs once at the start of the game
def startup():
    # enable depth test
    glEnable(GL_DEPTH_TEST)
    # enable smooth shading
    glShadeModel(GL_SMOOTH)

# Event handling
def handle_event(event):
    global cube_display
    # key down
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            if cube_display <= 0:
                cube_display = len(cube_drawing_functions)
            cube_display -= 1
            

# Draw runs after updates
def draw():
    cube_drawing_functions[cube_display]()