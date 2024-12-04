from game_logic import DIRECTIONS, change_direction
import threading

def read_keyboard(window, snake_head):
    while True:
        window.listen()
        window.onkeypress(lambda: change_direction(snake_head, DIRECTIONS[0]), DIRECTIONS[0])
        window.onkeypress(lambda: change_direction(snake_head, DIRECTIONS[1]), DIRECTIONS[1])
        window.onkeypress(lambda: change_direction(snake_head, DIRECTIONS[2]), DIRECTIONS[2])
        window.onkeypress(lambda: change_direction(snake_head, DIRECTIONS[3]), DIRECTIONS[3])

def setup_keyboard_reader(window, snake_head):
    '''
    Start the keyboard reading thread
    '''
    keyboard_thread = threading.Thread(target=read_keyboard, args=(window, snake_head))
    keyboard_thread.daemon = True
    keyboard_thread.start()