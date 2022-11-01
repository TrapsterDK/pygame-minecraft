import pygame
import pyrr
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from gameengine import quit_game

# https://learnopengl.com/Getting-started/Camera

camera_pos =    pyrr.Vector3([0.0, 0.0, 5.0])
camera_front =  pyrr.Vector3([0.0, 0.0, -1.0])
camera_up =     pyrr.Vector3([0.0, 1.0, 0.0])

yaw = -90.0
pitch = 0.0

sensitivity = 0.1
camera_speed = 0.1

def mouse_movement(event):
    global yaw, pitch, camera_front

    x, y = event.rel
    x *= sensitivity
    y = -y * sensitivity

    yaw += x
    pitch += y

    pitch = max(min(pitch, 89.0), -89.0)

    front = pyrr.Vector3([
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ])

    camera_front = pyrr.vector.normalise(front)

def key_movement():
    global camera_pos, camera_front, camera_up, camera_speed

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_pos += camera_front * camera_speed
    if keys[pygame.K_s]:
        camera_pos -= camera_front * camera_speed
    if keys[pygame.K_a]:
        camera_pos -= pyrr.vector.normalise(pyrr.vector3.cross(camera_front, camera_up)) * camera_speed
    if keys[pygame.K_d]:
        camera_pos += pyrr.vector.normalise(pyrr.vector3.cross(camera_front, camera_up)) * camera_speed
    if keys[pygame.K_SPACE]:
        camera_pos += camera_up * camera_speed
    if keys[pygame.K_LSHIFT]:
        camera_pos -= camera_up * camera_speed

# Statup runs once at the start of the game
def startup():
    # capture mouse
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    # set up projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = pygame.display.get_surface().get_size()
    gluPerspective(45, (width / height), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

# Update runs after event handling
# Takes delta time since last frame as argument
def update(delta_time):
    key_movement()  

    # update view matrix
    glLoadIdentity()
    gluLookAt(*camera_pos, *(camera_pos + camera_front), *camera_up)

# Event handling
def handle_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            quit_game()

    if event.type == pygame.MOUSEMOTION:
        mouse_movement(event)
