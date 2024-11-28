from main import window, snake
from game_logic import DIRECTIONS, change_direction
import threading

def read_keyboard():
    while True:
        window.listen()
        for direction in DIRECTIONS:
            window.onkeypress(lambda: change_direction(snake, direction), direction)

def setup_keyboard_reader():
    '''
    Start the keyboard reading thread
    '''
    keyboard_thread = threading.Thread(target=read_keyboard)
    keyboard_thread.daemon = True
    keyboard_thread.start()