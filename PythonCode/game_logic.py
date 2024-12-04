import time
import random
from setup import create_segment

score = 0
high_score = 0

DIRECTIONS = ["Up", "Left", "Down", "Right"]

def enemy_decide_direction(enemy_head):
    '''
    Selects a random direction for the enemy to move in that does not move it outside of the screen
    '''
    possible_directions = DIRECTIONS.copy()

    if enemy_head.xcor() > 270: possible_directions.remove("Right")
    if enemy_head.xcor() < -270: possible_directions.remove("Left")
    if enemy_head.ycor() > 270: possible_directions.remove("Up")
    if enemy_head.ycor() < -270: possible_directions.remove("Down")

    return random.choice(possible_directions)

def move(head, segments):
    '''
    Moves the entity
    '''
    if len(segments) > 0:
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    if head.direction == "Up":
        head.sety(head.ycor() + 20)
    if head.direction == "Down":
        head.sety(head.ycor() - 20)
    if head.direction == "Left":
        head.setx(head.xcor() - 20)
    if head.direction == "Right":
        head.setx(head.xcor() + 20)

def change_direction(head, direction):
    '''
    Sets the directen the entity will move next
    '''
    if head.direction == "Stop":
        head.direction = direction
        return

    index = (DIRECTIONS.index(head.direction) + (len(DIRECTIONS) / 2)) % len(DIRECTIONS)
    opposite_direction = DIRECTIONS[int(index)]

    if direction != opposite_direction:
        head.direction = direction

def reset_game(snake_head, snake_body, enemy_head, enemy_body, food, pen,):
    '''
    Resets the game
    '''
    def reset_head(head, shape, color, x, y, direction):
        head.speed(0)
        head.shape(shape)
        head.color(color)
        head.penup()
        head.goto(x, y)
        head.direction = direction

    time.sleep(1)
    global score, high_score
    
    for segment in snake_body:
        segment.goto(10000, 10000)
    snake_body.clear()

    for segment in enemy_body:
        segment.goto(10000, 10000)
    enemy_body.clear()

    x = random.randint(-290, 290)
    y = random.randint(-290, 290)
    food.goto(x, y)

    score = 0
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    reset_head(snake_head, "square", "black", 0, 0, "Stop")
    reset_head(enemy_head, "circle", "firebrick2", random.randint(-200, 200), random.randint(-200, 200), "Stop")

def check_death_collisions(snake_head, snake_body, enemy_head, enemy_body, food, pen):
    '''
    Checks for collisions that kill the player, and resets the game if they occur
    '''
    # Check for collision with body segments
    for segment in snake_body:
        if segment.distance(snake_head) < 10:
            reset_game(snake_head, snake_body, enemy_head, enemy_body, food, pen,)
    
    # Check for collision with border
    if snake_head.xcor() > 290 or snake_head.xcor() < -290 or snake_head.ycor() > 290 or snake_head.ycor() < -290:
        reset_game(snake_head, snake_body, enemy_head, enemy_body, food, pen,)

    # Check for collision with enemy segments and enemy head
    if enemy_head.distance(snake_head) < 20:
        reset_game(snake_head, snake_body, enemy_head, enemy_body, food, pen,)

    for segment in enemy_body:
        if snake_head.distance(segment) < 20:
            reset_game(snake_head, snake_body, enemy_head, enemy_body, food, pen,)
            
    for segment in snake_body:
        if enemy_head.distance(segment) < 20:
            reset_game(snake_head, snake_body, enemy_head, enemy_body, food, pen,)

def check_food_collision(snake_head, snake_body, enemy_head, enemy_body, food, pen):
    '''
    Check for collision with food
    '''
    global score, high_score
    
    if snake_head.distance(food) >= 20:
        return
    
    x = random.randint(-290, 290)
    y = random.randint(-290, 290)
    food.goto(x, y)

    snake_body.append(create_segment("square", "SlateBlue3", snake_head.xcor(), snake_head.ycor()))
    enemy_body.append(create_segment("circle", "firebrick2", enemy_head.xcor(), enemy_head.ycor()))

    score += 10

    if score > high_score:
        high_score = score

    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))