import tkinter as tk
import random

# Game settings
WIDTH = 500
HEIGHT = 400
PIPE_GAP = 150
GAME_REFRESH_RATE = 20  # 20ms is the default
GRAVITY = 0.25  # 0.2 is the default
JUMP_STRENGTH = 6  # 5 is the default

# Create main window and canvas
root = tk.Tk()
root.title("Floppy Totoro")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

# DEBUG Options
show_hitbox = True
show_debug = True
if show_debug:
    debug_info = canvas.create_text(WIDTH / 2, 40, text="", font=("Arial", 16))

# Bird Logic
bird_size = 64
if show_hitbox:
    bird_hitbox = canvas.create_rectangle(
        50, HEIGHT / 2, 50 + bird_size, HEIGHT / 2 + bird_size, fill="yellow"
    )

totoUp = tk.PhotoImage(file="assets/sprites_64/totoUp.png")
totoDown = tk.PhotoImage(file="assets/sprites_64/totoDown.png")
totoFalling = tk.PhotoImage(file="assets/sprites_64/totoFalling.png")

bird = canvas.create_image(
    50, HEIGHT / 2, image=totoUp, anchor="nw"
)  # image = starting sprite


def jump():
    global bird_y_velocity
    bird_y_velocity = -JUMP_STRENGTH  # Negative for upward jump


bird_y_velocity = 0


def update_bird():
    global bird_y_velocity
    bird_y_velocity += GRAVITY
    canvas.move(bird, 0, bird_y_velocity)
    if bird_y_velocity < 0:
        canvas.itemconfig(bird, image=totoUp)
    else:
        canvas.itemconfig(bird, image=totoDown)

    if show_debug:
        canvas.itemconfig(debug_info, text="Bird Y Velocity: " + str(bird_y_velocity))
    if show_hitbox:
        canvas.move(bird_hitbox, 0, bird_y_velocity)


# region Pipes
pipe_speed = 3  # Horizontal speed of pipes
pipe_width = 50
pipes = []  # List to store pipe rectangles


def create_pipes():
    top_y = random.randint(50, HEIGHT - PIPE_GAP - 50)
    bottom_y = top_y + PIPE_GAP
    top_rect = canvas.create_rectangle(
        WIDTH, 0, WIDTH + pipe_width, top_y, fill="green"
    )
    bottom_rect = canvas.create_rectangle(
        WIDTH, bottom_y, WIDTH + pipe_width, HEIGHT, fill="green"
    )

    pipe = {
        "top": top_rect,
        "bottom": bottom_rect,
    }
    pipes.append(pipe)


def move_pipes():
    for pipe in pipes:
        if canvas.coords(pipe["top"])[2] < 0:
            canvas.delete(pipe["top"])
            canvas.delete(pipe["bottom"])
            pipes.remove(pipe)
        else:
            canvas.move(pipe["top"], -pipe_speed, 0)
            canvas.move(pipe["bottom"], -pipe_speed, 0)


# endregion

# region Score
score = 0
score_display = canvas.create_text(WIDTH / 2, 20, text="Score: 0", font=("Arial", 16))


def update_score():
    global score
    score += 1
    canvas.itemconfig(score_display, text="Score: " + str(score))
    canvas.tag_raise(score_display)


# endregion

# region Game Logic
game_running = True


def game_over():
    global game_running
    game_running = False
    canvas.itemconfig(bird, image=totoFalling)
    canvas.move(bird, 0, 5)
    canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", font=("Arial", 24))


def check_collision():
    global bird_size
    bird_coords = canvas.coords(bird)
    if len(bird_coords) == 2:
        bird_coords = [
            bird_coords[0],
            bird_coords[1],
            bird_coords[0] + bird_size,
            bird_coords[1] + bird_size,
        ]

    for pipe in pipes:
        top_coords = canvas.coords(pipe["top"])
        bottom_coords = canvas.coords(pipe["bottom"])
        # print(bird_coords)

        # bird_coords[0] is left, bird_coords[1] is top, bird_coords[2] is right, bird_coords[3] is bottom
        # coords[0] is left, coords[1] is top, coords[2] is right, coords[3] is bottom
        if (
            bird_coords[2]
            > top_coords[
                0
            ]  # if the right side of the bird is to the right of the left side of the top pipe
            and bird_coords[0]
            < top_coords[
                2
            ]  # if the left side of the bird is to the left of the right side of the top pipe
            and bird_coords[3]
            > top_coords[
                1
            ]  # if the bottom of the bird is below the top of the top pipe
            and bird_coords[1]
            < top_coords[
                3
            ]  # if the top of the bird is above the bottom of the top pipe
        ):
            game_over()

        # Check for collision with bottom pipe
        if (
            bird_coords[2] > bottom_coords[0]
            and bird_coords[0] < bottom_coords[2]
            and bird_coords[1] < bottom_coords[3]
            and bird_coords[3] > bottom_coords[1]
        ):
            game_over()

        if (
            bird_coords[3] > HEIGHT or bird_coords[1] < 0
        ):  # Check for collision with top or bottom of the screen
            game_over()

        # Check for passing the pipe
        if bird_coords[0] > top_coords[2]:
            update_score()


def game_over_animation():
    root.unbind("<space>")
    global bird_y_velocity
    if canvas.coords(bird)[1] < HEIGHT + bird_size:
        bird_y_velocity += GRAVITY
        canvas.move(bird, 0, bird_y_velocity)
        if show_hitbox:
            canvas.move(bird_hitbox, 0, bird_y_velocity)
        root.after(GAME_REFRESH_RATE, game_over_animation)


def game_loop(first_run=False, start_message=None):
    if not game_running:
        game_over_animation()
        return
    elif first_run:
        jump()
        root.bind("<space>", lambda event: jump())
        canvas.delete(start_message)
    update_bird()

    # Create new pipes periodically
    if len(pipes) == 0 or canvas.coords(pipes[-1]["top"])[2] < WIDTH - 300:
        create_pipes()

    move_pipes()
    check_collision()

    root.after(GAME_REFRESH_RATE, game_loop)


def start_screen():
    start_message = canvas.create_text(
        WIDTH / 2, HEIGHT / 2, text="Press Space to Start", font=("Arial", 24)
    )
    root.bind(
        "<space>", lambda event: game_loop(first_run=True, start_message=start_message)
    )


# endregion
start_screen()
root.mainloop()  # Start main loop
