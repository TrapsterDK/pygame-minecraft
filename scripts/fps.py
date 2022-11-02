import pygame
import moderngl
from array import array
from gameengine import get_clock, get_gl_context

IGNORE_MODULE = 1

LEFT = 1
RIGHT = 2
TOP = 4
BOTTOM = 8

ENABLED = True

counter_position = LEFT | TOP

def set_position(position: int) -> None:
    global counter_position
    counter_position = position

def set_fps_counter_enabled(enabled: bool) -> None:
    global ENABLED
    ENABLED = enabled

def draw():
    if not ENABLED:
        return
        
    ctx = get_gl_context()

    fps = int(get_clock().get_fps())
    
    # pygame surface
    surface = pygame.font.SysFont(None, 20).render(f"FPS: {fps:3d}", True, (255, 255, 255, 255)).convert_alpha()
    data = pygame.image.tostring(surface, "RGBA", True)

    # size
    w, h = pygame.display.get_surface().get_size()
    tw, th = surface.get_size()

    # text draw to screen using moderngl
    texture = ctx.texture((tw, th), 4, data=data)
    texture.use()

    program = ctx.program(
        vertex_shader='''
            #version 330
            in vec2 in_vert;
            in vec2 in_text;
            out vec2 v_text;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
                v_text = in_text;
            }
        ''',
        fragment_shader='''
            #version 330
            uniform sampler2D Texture;
            in vec2 v_text;
            out vec4 f_color;
            void main() {
                f_color = texture(Texture, v_text);
            }
        ''',
    )

    vbo = ctx.buffer(array('f', [
        # Position (x, y) , Texture coordinates (x, y)
        -1.0, 1.0, 0.0, 1.0,  # upper left
        -1.0, -1.0, 0.0, 0.0,  # lower left
        1.0, 1.0, 1.0, 1.0,  # upper right
        1.0, -1.0, 1.0, 0.0,  # lower right
    ]))

    vao = ctx.vertex_array(program, [(vbo, '2f 2f', 'in_vert', 'in_text')])

    # draw to screen
    if counter_position & LEFT:
        x = 0
    elif counter_position & RIGHT:
        x = w - tw
    else:   
        x = (w - tw) / 2

    if counter_position & TOP:
        y = 0
    elif counter_position & BOTTOM:
        y = h - th
    else:
        y = (h - th) / 2

    ctx.viewport = (0, 0, w, h)
    vao.render()    
