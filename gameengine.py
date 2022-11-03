from typing import Callable
import pygame
import pathlib
import importlib
from types import ModuleType
from settings import SCREEN_SIZE_DEFAULT, FPS_MAX_DEFAULT, SCRIPTS_FOLDER, GAME_TITLE, CLEAR_COLOR, SHADER_FOLDER, TEXTURE_FOLDER
import moderngl
from PIL import Image


IGNORE_MODULE = 'IGNORE_MODULE'


max_fps:        int = FPS_MAX_DEFAULT
callbacks_set:  bool = False
clear_color:    tuple[float, float, float] = None
gl_context:     moderngl.Context = None
clock:          pygame.time.Clock = None


# loads single texture in rgba format
def load_texture(path: str) -> moderngl.Texture:
    # load image as rgba
    image = Image.open(f'{TEXTURE_FOLDER}/{path}').convert('RGBA')

    # flip for opengl
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # create texture
    texture = gl_context.texture(image.size, 4, image.tobytes())

    return texture


# load vertex and fragment shader into program
def get_shader(shader_name: str) -> moderngl.Program:
    return gl_context.program(
        vertex_shader = open(f"{SHADER_FOLDER}/{shader_name}.vs").read(),
        fragment_shader = open(f"{SHADER_FOLDER}/{shader_name}.fs").read()
    )


# get gl context
def get_gl_context() -> moderngl.Context:
    return gl_context


# get pygame clock
def get_clock() -> pygame.time.Clock:
    return clock


# set max fps
def set_max_fps(new_fps: int) -> None:
    global max_fps
    max_fps = new_fps


# set clear color
def set_clear_color(color: tuple[int, int, int]) -> None:
    global clear_color
    clear_color = (*[c/255 for c in color], 1)


# post quit game event
def quit_game() -> None:
    event = pygame.event.Event(pygame.QUIT)
    pygame.event.post(event)


# start game
def start_game(specific_module: str = None) -> None:
    global gl_context, clock
    
    # set clear color
    set_clear_color(CLEAR_COLOR)

    # load all scripts
    if specific_module is None:
        modules = _import_scripts()
        
        # check if module should be ignored
        for module in reversed(modules):
            if hasattr(module, IGNORE_MODULE):
                # check if set to ignore
                if getattr(module, IGNORE_MODULE):
                    modules.remove(module)

    # load specific script
    else:
        modules = [importlib.import_module(f"{SCRIPTS_FOLDER}.{specific_module}")]

    # get callbacks
    startup_callback = _get_modules_function(modules, 'startup')
    cleanup_callback = _get_modules_function(modules, 'cleanup')
    update_callback = _get_modules_function(modules, 'update')
    handle_event_callback = _get_modules_function(modules, 'handle_event')
    draw_callback = _get_modules_function(modules, 'draw')
            
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode(SCREEN_SIZE_DEFAULT, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    # moderngl
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    # context
    gl_context = moderngl.create_context()

    clock = pygame.time.Clock()

    # game statup
    for callback in startup_callback:
        callback()

    running = True
    while running:
        # cap fps, and get delta time
        delta_time = clock.tick(max_fps)

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # call all handle event callbacks
            for callback in handle_event_callback:
                callback(event)
        
        # call all update callbacks
        for callback in update_callback:
            callback(delta_time)

        # clear screen
        gl_context.clear(*clear_color)

        # call all draw callbacks
        for callback in draw_callback:
            callback()

        # update screen
        pygame.display.flip()

    # game cleanup
    for callback in cleanup_callback:
        callback()
    
    # quit pygame
    pygame.quit()
    quit()


# load all scripts
def _import_scripts() -> list[ModuleType]:
    scripts = []
    for script in pathlib.Path(SCRIPTS_FOLDER).iterdir():
        if script.suffix == '.py':
            scripts.append(importlib.import_module(f"{SCRIPTS_FOLDER}.{script.stem}"))
    return scripts


# get function from scripts
def _get_modules_function(modules: list[ModuleType], function: str) -> list[Callable]:
    functions = []
    for module in modules:
        if hasattr(module, function):
            functions.append(getattr(module, function))

    return functions