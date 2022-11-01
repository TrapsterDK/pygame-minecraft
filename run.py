from importer import load_functions
from gameengine import start_game, set_callbacks

def run():
    functions = load_functions()
    set_callbacks(**functions)
    start_game()

if __name__ == "__main__":
    run()