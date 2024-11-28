from setup import create_segment, setup_game_window, setup_pen
from serial_connection import setup_serial_connection, create_arduino_thread, weight_adjusted_interval
from game_logic import move, reset_game, check_death_collisions, check_food_collision, enemy_decide_direction
import turtle
import time
import random

score = 0
high_score = 0

MAX_UPDATE_INTERVAL = 0.35
player_update_interval = MAX_UPDATE_INTERVAL
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

enemy_start_x = random.randint(-200, 200)
enemy_start_y = random.randint(-200, 200)
enemy_head = create_segment("circle", "firebrick2", enemy_start_x, enemy_start_y, "stop")
enemy_body = []

food_start_x = random.randint(-200, 200)
food_start_y = random.randint(-200, 200)
food = create_segment("turtle", "black", food_start_x,food_start_y)

def game_loop():
    global time_last_update, player_update_timer, enemy_update_timer

    time_delta = time.time() - time_last_update
    time_last_update = time.time()

    player_update_timer += time_delta
    enemy_timer += time_delta

    if player_update_timer >= player_update_interval:
        move(snake_head, snake_body)
        player_update_timer = 0
    
    if enemy_timer >= enemy_update_interval:
        enemy_head.direction = enemy_decide_direction()
        move(enemy_head, enemy_body)
        enemy_timer = 0

    check_death_collisions()
    check_food_collision()
    
    window.update()

    turtle.ontimer(game_loop, int(1000 / 30))

window.mainloop()