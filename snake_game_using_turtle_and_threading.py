import turtle
import threading
import time
import random
import serial

""" # Initialize serial communication
arduino = serial.Serial('/dev/ttyACM0', 9600)  # Replace '/dev/ttyACM0' with your Arduino's serial port """

delay = 0.1
# Score
score = 0
high_score = 0

# Set up the window
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("light green")
wn.setup(width=600, height=600)
wn.tracer(0)

# Reset head
def reset_head(head, shape, color, x, y, direction):
    head.speed(0)
    head.shape(shape)
    head.color(color)
    head.penup()
    head.goto(x, y)
    head.direction = direction

# Add one segment to a segments list
def add_segment(segments, color, shape):
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape(shape)
    new_segment.color(color)
    new_segment.penup()
    segments.append(new_segment)


# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("turtle")
food.color("black")
food.penup()
food.goto(random.randint(-200, 200), random.randint(-200, 200))


# Snake head
snake_head = turtle.Turtle()
reset_head(snake_head, "square", "black", 0, 0, "stop")

# Snake body
snake_segments = []

# Ennemy head
ennemy_head = turtle.Turtle()
x = random.randint(-200, 200)
y = random.randint(-200, 200)
reset_head(ennemy_head, "circle", "firebrick2", x, y, "stop")

# Ennemy body
ennemy_segments = []


# Pen (score)
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions to control the snake
def go_up(head):
    if head.direction != "down":
        head.direction = "up"
def go_down(head):
    if head.direction != "up":
        head.direction = "down"
def go_left(head):
    if head.direction != "right":
        head.direction = "left"
def go_right(head):
    if head.direction != "left":
        head.direction = "right"

# Move head function
def move_head(head):
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

# Move body function
def move_body(segments, head):
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

# Reset game
def reset_game():
    global score, delay, snake_segments
    time.sleep(1)
    reset_head(snake_head, "square", "black", 0, 0, "stop")
    reset_head(ennemy_head, "circle", "firebrick2", random.randint(-200, 200), random.randint(-200, 200), "stop")
    for segment in snake_segments:
        segment.goto(10000, 10000)
    snake_segments.clear()
    for segment in ennemy_segments:
        segment.goto(10000, 10000)
    ennemy_segments.clear()

    x = random.randint(-290, 290)
    y = random.randint(-290, 290)
    food.goto(x, y)

    score = 0
    delay = 0.1
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

# Game loop
def game_loop():
    global delay, score, high_score

    wn.update()

    # Check for collision with border
    if snake_head.xcor() > 290 or snake_head.xcor() < -290 or snake_head.ycor() > 290 or snake_head.ycor() < -290:
        reset_game()
    if ennemy_head.xcor() > 290: go_left(ennemy_head)
    if ennemy_head.xcor() < -290: go_right(ennemy_head)
    if ennemy_head.ycor() > 290: go_down(ennemy_head)
    if ennemy_head.ycor() < -290: go_up(ennemy_head)

    # Check for collision with food
    if snake_head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        add_segment(snake_segments, "SlateBlue3", "square")
        add_segment(ennemy_segments, "firebrick2", "circle")

        # The snake is going faster
        delay -= 0.0001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))


    # Move the snake segments
    move_body(snake_segments, snake_head)
    move_head(snake_head)

    # Move the ennemy segments
    move_body(ennemy_segments, ennemy_head)
    ennemy_direction = random.choice(["up", "down", "left", "right"])
    ennemy_head.direction = ennemy_direction
    move_head(ennemy_head)

    # Check for collision with body segments
    for segment in snake_segments:
        if segment.distance(snake_head) < 10:
            reset_game()

    # Check for collision with ennemy segments and ennemy head
    if ennemy_head.distance(snake_head) < 20:
            reset_game()
    for segment in ennemy_segments:
        if segment.distance(snake_head) < 20:
            reset_game()
    for segment in snake_segments:
        if segment.distance(ennemy_head) < 20:
            reset_game()
    for ennemy_segment in ennemy_segments:
        for snake_segment in snake_segments:
            if ennemy_segment.distance(snake_segment) < 20:
                reset_game()

    turtle.ontimer(game_loop, int(delay * 1000))



# Read input
def read_arduino():
    while True:
        wn.listen() 
        wn.onkeypress(lambda: go_up(snake_head), "Up")
        wn.onkeypress(lambda: go_down(snake_head), "Down")
        wn.onkeypress(lambda: go_left(snake_head), "Left")
        wn.onkeypress(lambda: go_right(snake_head), "Right")
"""         if arduino.in_waiting > 0:
            data = arduino.readline().decode().strip()
            if data == 'UP':
                go_up()
            elif data == 'DOWN':
                go_down()
            elif data == 'LEFT':
                go_left()
            elif data == 'RIGHT':
                go_right() """
        

# Start the Arduino reading thread
arduino_thread = threading.Thread(target=read_arduino)
arduino_thread.daemon = True
arduino_thread.start()

# Start the game loop
game_loop()

wn.mainloop()
