import turtle

def create_segment(shape, color, x, y):
    '''
    Creates the head of an entety
    '''
    head = turtle.Turtle()
    head.speed(0)
    head.shape(shape)
    head.color(color)
    head.penup()
    head.goto(x, y)
    head.direction = "Stop"
    return head

def setup_pen():
    # Pen (score)
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("black")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))
    return pen

def setup_game_window(title, bg_color, width, height):
    '''
    Set up the game window
    '''
    window = turtle.Screen()
    window.title(title)
    window.bgcolor(bg_color)
    window.setup(width, height)
    window.tracer(0)
    return window