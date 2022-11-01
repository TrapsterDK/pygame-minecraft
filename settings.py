from pygame import RESIZABLE, OPENGL

# Console Debugging
DEBUG = True
LOGGING_FILE = "log.txt"

# Folder where scripts are stored
SCRIPTS_FOLDER = 'scripts'

# Game title
GAME_TITLE = "Game"

# Default screen size
SCREEN_SIZE_DEFAULT = (800, 600)

# Default fps, set to 0 to disable fps limit
FPS_MAX_DEFAULT = 60

# Flags for pygame.display.set_mode, already includes DOUBLEBUF
FLAGS = RESIZABLE | OPENGL

# Weather to display fps in left top corner
FPS_COUNTER = True

# Default clear color
CLEAR_COLOR = (173, 216, 230) #light blue