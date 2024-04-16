import tkinter as tk
import random

# Game settings
WIDTH = 500
HEIGHT = 400
PIPE_GAP = 150

# Create main window and canvas
root = tk.Tk()
root.title("Floppy Totoro")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

# Bird Logic
bird_size = 20
bird = canvas.create_rectangle(
    50, HEIGHT / 2, 50 + bird_size, HEIGHT / 2 + bird_size, fill="yellow"
)

gravity = 0.2
bird_y_velocity = 0


def jump():
    global bird_y_velocity
    bird_y_velocity = -8  # Negative for upward jump


root.bind("<space>", lambda event: jump())


def update_bird():
    global bird_y_velocity
    bird_y_velocity += gravity
    canvas.move(bird, 0, bird_y_velocity)


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


# endregion

# region Game Logic
game_running = True


def game_over():
    global game_running
    game_running = False
    canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", font=("Arial", 24))
    # root.quit()


def check_collision():
    bird_coords = canvas.coords(bird)
    for pipe in pipes:
        top_coords = canvas.coords(pipe["top"])
        bottom_coords = canvas.coords(pipe["bottom"])
        # print(bird_coords)

        # bird_coords[0] is left, bird_coords[1] is top, bird_coords[2] is right, bird_coords[3] is bottom
        # coords[0] is left, coords[1] is top, coords[2] is right, coords[3] is bottom
        # 0, 0 is top left corner
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
            print(top_coords, bottom_coords)
            print("Collision with top pipe")
            game_over()

        # Check for collision with bottom pipe
        if (
            bird_coords[2] > bottom_coords[0]
            and bird_coords[0] < bottom_coords[2]
            and bird_coords[1] < bottom_coords[3]
            and bird_coords[3] > bottom_coords[1]
        ):
            print(top_coords, bottom_coords)
            print("Collision with bottom pipe")
            game_over()

        # Check for passing the pipe
        if bird_coords[0] > top_coords[2]:
            update_score()


def game_loop():
    if not game_running:
        return
    update_bird()
    move_pipes()
    check_collision()

    # Create new pipes periodically
    if len(pipes) == 0 or canvas.coords(pipes[-1]["top"])[2] < WIDTH - 300:
        create_pipes()

    root.after(20, game_loop)  # Adjust '20' for game speed


# endregion

# Call functions to start the game
game_loop()
root.mainloop()  # Start main loop
