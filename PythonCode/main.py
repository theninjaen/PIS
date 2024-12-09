from setup import create_segment, setup_game_window, setup_pen
from keyboard_control import setup_keyboard_reader
from serial_connection import setup_serial_connection, create_arduino_thread, read_weight_adjusted_interval, read_heart_rate, MAX_UPDATE_INTERVAL
from game_logic import move, check_death_collisions, check_food_collision, enemy_decide_direction
import turtle
import time
import random

player_update_timer = 0

enemy_update_interval = MAX_UPDATE_INTERVAL
enemy_update_timer = 0

time_last_update = time.time()

setup_serial_connection("COM4", 9600)
create_arduino_thread()

window = setup_game_window("Snake", "light green", 600, 600)

pen = setup_pen()

snake_head = create_segment("square", "black", 0, 0)
snake_body = []

setup_keyboard_reader(window, snake_head)

enemy_start_x = random.randint(-20, 20) * 10
enemy_start_y = random.randint(-20, 20) * 10
enemy_head = create_segment("circle", "firebrick2", enemy_start_x, enemy_start_y)
enemy_body = []

food_start_x = random.randint(-20, 20) * 10
food_start_y = random.randint(-20, 20) * 10
food = create_segment("turtle", "black", food_start_x,food_start_y)

def game_loop():
    global time_last_update, player_update_timer, enemy_update_timer

    time_delta = time.time() - time_last_update
    time_last_update = time.time()

    player_update_timer += time_delta
    enemy_update_timer += time_delta

    if player_update_timer >= read_weight_adjusted_interval():
        check_food_collision(snake_head, snake_body, enemy_head, enemy_body, food, pen)
        move(snake_head, snake_body)
        player_update_timer = 0
    
    if enemy_update_timer >= read_heart_rate():
        enemy_head.direction = enemy_decide_direction(enemy_head)
        move(enemy_head, enemy_body)
        enemy_update_timer = 0

    check_death_collisions(snake_head, snake_body, enemy_head, enemy_body, food, pen)
    
    window.update()

    turtle.ontimer(game_loop, int(1000 / 30))

game_loop()

window.mainloop()