from gameengine import start_game
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_game(sys.argv[1])
    else:
        start_game()