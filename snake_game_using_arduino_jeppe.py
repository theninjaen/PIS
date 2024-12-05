import turtle
import PySimpleGUI as sg
import threading
import time
import random
import sys
import queue
import serial

# Set up serial communication
try:
    ser = serial.Serial('COM4', baudrate=9600, timeout=1)
    ser.flushInput()
    shouldRead = True
except serial.SerialException:
    print('Serial port not found.... Check USB connection', file=sys.stderr)
    shouldRead = False 
latest_weight = 0
instant_weight = 0

# Delays
game_delay = 0.5
player_delay = 0.5
enemy_delay = 0.5

# Initialize queues
arduino_queue = queue.Queue()
heartrate_queue = queue.Queue()

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

# Enemy head
enemy_head = turtle.Turtle()
x = random.randint(-200, 200)
y = random.randint(-200, 200)
reset_head(enemy_head, "circle", "firebrick2", x, y, "stop")

# Enemy body
enemy_segments = []

# Pen (score)
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Pen (weight)
pen_weight = turtle.Turtle()
pen_weight.speed(0)
pen_weight.shape("square")
pen_weight.color("black")
pen_weight.penup()
pen_weight.hideturtle()
pen_weight.goto(0, -260)
pen_weight.write("Delay: 0", align="center", font=("Courier", 24, "normal"))

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
    global score, game_delay, snake_segments
    time.sleep(1)
    reset_head(snake_head, "square", "black", 0, 0, "stop")
    reset_head(enemy_head, "circle", "firebrick2", random.randint(-200, 200), random.randint(-200, 200), "stop")
    for segment in snake_segments:
        segment.goto(10000, 10000)
    snake_segments.clear()
    for segment in enemy_segments:
        segment.goto(10000, 10000)
    enemy_segments.clear()

    x = random.randint(-290, 290)
    y = random.randint(-290, 290)
    food.goto(x, y)

    score = 0
    game_delay = 0.5
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

# Game loop
def game_loop():
    global game_delay, score, high_score, enemy_delay, player_delay

    wn.update()

    while not arduino_queue.empty():
        instant_weight = arduino_queue.get()
        weight_change = instant_weight - latest_weight  
        player_delay = max(0.1, player_delay - 0.005 * weight_change)

    # while not heartrate_queue.empty():
    #     heart_rate = heartrate_queue.get()
    #     if heart_rate > 80:
    #         enemy_delay = max(0.1, enemy_delay - 0.02 * (heart_rate - 80))
    #     else:
    #         enemy_delay = 0.5

    # Check for collision with border
    if snake_head.xcor() > 290 or snake_head.xcor() < -290 or snake_head.ycor() > 290 or snake_head.ycor() < -290:
        reset_game()
    if enemy_head.xcor() > 290: go_left(enemy_head)
    if enemy_head.xcor() < -290: go_right(enemy_head)
    if enemy_head.ycor() > 290: go_down(enemy_head)
    if enemy_head.ycor() < -290: go_up(enemy_head)

    # Check for collision with food
    if snake_head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        add_segment(snake_segments, "SlateBlue3", "square")
        add_segment(enemy_segments, "firebrick2", "circle")
        game_delay -= 0.0001
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Move the snake segments
    move_body(snake_segments, snake_head)
    move_head(snake_head)

    # Move the enemy segments
    move_body(enemy_segments, enemy_head)
    enemy_direction = random.choice(["up", "down", "left", "right"])
    enemy_head.direction = enemy_direction
    move_head(enemy_head)

    pen_weight.clear()
    pen_weight.write("Delay: {}".format(game_delay), align="center", font=("Courier", 24, "normal"))

    # Check for collision with body segments
    for segment in snake_segments:
        if segment.distance(snake_head) < 10:
            reset_game()
    if enemy_head.distance(snake_head) < 20:
        reset_game()
    for segment in enemy_segments:
        if segment.distance(snake_head) < 20:
            reset_game()
    for segment in snake_segments:
        if segment.distance(enemy_head) < 20:
            reset_game()
    for enemy_segment in enemy_segments:
        for snake_segment in snake_segments:
            if enemy_segment.distance(snake_segment) < 10:
                reset_game()
                break

    # Schedule next game loop
    turtle.ontimer(game_loop, int(game_delay * 1000))

# Thread to read data from Arduino
def read_arduino():
    global latest_weight, instant_weight
    while shouldRead:
        data = ser.readline().decode().strip()
        if data.isdigit():
            latest_weight = instant_weight
            instant_weight = int(data)
            arduino_queue.put(instant_weight)
        time.sleep(1)

# Heart rate display function
def read_heart_rate():
    while True:
        layout = [
            [sg.Text("Your Heart Rate is"), sg.Text("", key="-OUTPUT-")],
            [sg.Button("OK")]
        ]
        window = sg.Window("Heart Rate", layout)
        for i in range(80, 120):
            heartrate_queue.put(i)
            event, values = window.read(timeout=100)
            window["-OUTPUT-"].update(i)
            if event == "OK" or event == sg.WIN_CLOSED:
                break
        window.close()

# Set up controls
wn.listen()
wn.onkeypress(lambda: go_up(snake_head), "w")
wn.onkeypress(lambda: go_down(snake_head), "s")
wn.onkeypress(lambda: go_left(snake_head), "a")
wn.onkeypress(lambda: go_right(snake_head), "d")

# Start threads
arduino_thread = threading.Thread(target=read_arduino)
arduino_thread.start()
# heartrate_thread = threading.Thread(target=read_heart_rate)
# heartrate_thread.start()

# Start game loop
game_loop()

# Main event loop
wn.mainloop()
