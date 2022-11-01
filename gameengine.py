# pip install PyOpenGL PyOpenGL_accelerate pygame

from typing import Any, Callable
import pygame
from utils import debug_log, GAME_WRAPPER
from settings import SCREEN_SIZE_DEFAULT, FPS_MAX_DEFAULT, FLAGS, GAME_TITLE, FPS_COUNTER, CLEAR_COLOR
from OpenGL.GL import glWindowPos2d, glDrawPixels, glBlendFunc, glEnable, glClear, glClearColor, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_BLEND, GL_RGBA, GL_UNSIGNED_BYTE

clock:                  pygame.time.Clock = None
fps:                    int = FPS_MAX_DEFAULT
callbacks_set:          bool = False
opengl:                 bool = FLAGS & pygame.OPENGL # if opengl is enabled
clear_color:            tuple[int, int, int] = CLEAR_COLOR

startup_callback:       list[Callable] = None
pre_update_callback:    list[Callable] = None
update_callback:        list[Callable] = None
handle_events_callback: list[Callable] = None
draw_callback:          list[Callable] = None
cleanup_callback:       list[Callable] = None 


def get_fps() -> int:
    return fps

def set_fps(new_fps: int):
    global fps
    fps = new_fps

def set_clear_color(color: tuple[int, int, int]):
    global clear_color

    if opengl:
        glClearColor(*[c/255 for c in color], 1)

    clear_color = color

def quit_game():
    event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(event)

def set_callbacks(
        startup: list[Callable],
        pre_update: list[Callable],
        update: list[Callable], 
        handle_event: list[Callable],
        draw: list[Callable],
        cleanup: list[Callable]
    ):
    global callbacks_set, startup_callback, pre_update_callback, update_callback, handle_events_callback, draw_callback, cleanup_callback

    startup_callback = startup
    pre_update_callback = pre_update
    update_callback = update
    handle_events_callback = handle_event
    draw_callback = draw
    cleanup_callback = cleanup

    callbacks_set = True
    debug_log(GAME_WRAPPER, "Set callbacks")


def start_game():
    if not callbacks_set:
        raise Exception("Callbacks not set, before starting the game")

    global clock
            
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    pygame.display.set_mode(SCREEN_SIZE_DEFAULT, pygame.DOUBLEBUF | FLAGS)

    if opengl:
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    clock = pygame.time.Clock()

    debug_log(GAME_WRAPPER, "Pygame initialized")

    # game statup
    _startup()
    debug_log(GAME_WRAPPER, "Startup functions done")

    debug_log(GAME_WRAPPER, "Starting game loop")

    while True:
        delta_time = clock.tick(fps)

        _pre_update()
        if _handle_events(): # if the game should closes
            break
        _update(delta_time)

        _draw()

        # create fps counter if enabled
        if FPS_COUNTER:
            # rgba for opengl support
            text_surface = pygame.font.SysFont(None, 20).render(f"FPS: {int(clock.get_fps()):3d}", True, (255, 255, 255, 255))
            if opengl:
                # convert surface to opengl texture
                text_surface = text_surface.convert_alpha()
                text_data = pygame.image.tostring(text_surface, "RGBA", True)

                # draw texture in top left corner, calculate position as openl coordinates start in the bottom left corner
                w, h = pygame.display.get_surface().get_size()
                tw, th = text_surface.get_size()
                glWindowPos2d(0, h-th)
                glDrawPixels(tw, th, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
            else:
                pygame.display.get_surface().blit(text_surface, (0, 0))

        pygame.display.flip()

    _cleanup()
    debug_log(GAME_WRAPPER, "Cleanup functions dones")

    pygame.quit()
    debug_log(GAME_WRAPPER, "Pygame closed")
    quit()

# runs all callbacks
def _callbacks(callbacks: list[Callable], *args: Any):
    for callback in callbacks:
        callback(*args)

# updates before event handling and update
def _pre_update() -> bool:
    return _callbacks(pre_update_callback)

# updates after event handling
def _update(delta_time: float) -> bool:   
    return _callbacks(update_callback, delta_time)

# runs all startup callbacks
def _startup():
    _callbacks(startup_callback)

# runs all cleanup callbacks
def _cleanup():
    _callbacks(cleanup_callback)

# returns true if the game should close
def _handle_events() -> int:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True

        _callbacks(handle_events_callback, event)
    
    return False

# draws the screen
def _draw():
    # clear screen
    if opengl:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    else:
        pygame.display.get_surface().fill(clear_color)
    _callbacks(draw_callback)