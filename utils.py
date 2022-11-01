from settings import DEBUG, LOGGING_FILE


ERROR = "ERROR"
WARNING = "WARNING"
IMPORT = "IMPORT"
GAME_WRAPPER = "GAME WRAPPER"


#https://realpython.com/python-logging/
# debug loggig
def debug_log(print_type: str, *args):
    if DEBUG:
        print(f"{f'{print_type}:':15}", *args)
        with open(LOGGING_FILE, "a") as f:
            print(f"{f'{print_type}:':15}", *args, file=f)