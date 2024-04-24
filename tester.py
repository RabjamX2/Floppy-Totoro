""" tester.py """

import tkinter as tk
import random


def check_coord_collision(hitbox_coord, coords_to_check_against):
    """
    Check for collision between a hitbox coordinate and a list of coordinates.

    Args:
        hitboxCoord (list): The hitbox coordinate to check against.
        coordsToCheckAgainstList (list): The list of coordinates to check against.

    Returns:
        list: A list of collision results, where each result is a list containing a boolean value indicating collision and a string describing the collision.

    """
    result = []
    for coord_to_check_against in coords_to_check_against:
        if (
            hitbox_coord[2] > coord_to_check_against[0]
            and hitbox_coord[0] < coord_to_check_against[2]
            and hitbox_coord[3] > coord_to_check_against[1]
            and hitbox_coord[1] < coord_to_check_against[3]
        ):
            result.append([True, "Hit the object"])
        elif hitbox_coord[3] > 800:  # Change 800 to dynamic value
            result.append([True, "Hit the bottom of the screen"])
        elif hitbox_coord[1] < 0:
            result.append([True, "Hit the top of the screen"])
        elif hitbox_coord[0] > coord_to_check_against[2]:
            result.append([False, "Passed the pipe"])
        else:
            result.append([False, "No collision"])
    return result


class DebugInfo(tk.Text):
    """
    A custom text widget for displaying debug information.

    Args:
        parent (tkinter.Tk): The parent widget.

    """

    def __init__(self, parent):
        tk.Text.__init__(self, parent)
        self.parent = parent

        self.insert("1.0", "Debug Info\n")
        self.insert("2.0", "Hello\n")

        self.pack()

    def update_debug_text(self, new_text):
        """
        Update the debug text with new text.

        Args:
            newText (str): The new text to display.

        """
        self.debugText.set(newText)


class GameWindow(tk.Frame):
    """
    The main game window.

    Args:
        root (tkinter.Tk): The root widget.

    """

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root  # Not used right now
        self.windowWidth = 800
        self.windowHeight = 800

        self.gameBackground = GameBackground(
            self, width=self.windowWidth, height=self.windowHeight, bg="skyblue"
        )
        self.gameBackground.pack()


class GameBackground(tk.Canvas):
    """
    The game background canvas.

    Args:
        parent (tkinter.Frame): The parent widget.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    """

    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent


class Pipe:
    """
    A pipe object in the game.

    Args:
        parent (tkinter.Frame): The parent widget.
        canvas (tkinter.Canvas): The canvas to draw the pipe on.
        xOffset (int): The x-coordinate offset of the pipe.
        pipe_gap (int): The gap between the top and bottom pipes.
        pipe_width (int): The width of the pipe.

    """

    def __init__(self, parent, canvas, xOffset, pipe_gap, pipe_width):
        self.parent = parent
        self.canvas = canvas

        self.pipe_gap = pipe_gap
        self.pipe_width = pipe_width

        self.pointGiven = False

        self.top_y = random.randint(50, self.parent.windowHeight - self.pipe_gap - 50)
        self.bottom_y = self.top_y + self.pipe_gap

        self.top = self.canvas.create_rectangle(
            xOffset,
            0,
            xOffset + self.pipe_width,
            self.top_y,
            fill="green",
        )
        self.bottom = self.canvas.create_rectangle(
            xOffset,
            self.bottom_y,
            xOffset + self.pipe_width,
            self.parent.windowHeight,
            fill="green",
        )
        self.updateCurrentCoords()

    def updateCurrentCoords(self):
        """
        Update the current coordinates of the pipe.

        """
        self.top_coords = self.canvas.coords(self.top)
        self.bottom_coords = self.canvas.coords(self.bottom)

    def movePipe(self, pipe_speed):
        """
        Move the pipe horizontally.

        Args:
            pipe_speed (int): The speed at which the pipe moves.

        """
        self.canvas.move(self.top, -pipe_speed, 0)
        self.canvas.move(self.bottom, -pipe_speed, 0)
        self.updateCurrentCoords()

    def checkPipeCollision(self, birdCoords):
        """
        Check for collision between the bird and the pipe.

        Args:
            birdCoords (list): The coordinates of the bird.

        Returns:
            bool: True if there is a collision, False otherwise.

        """
        for checks in check_coord_collision(
            birdCoords, [self.top_coords, self.bottom_coords]
        ):
            if checks[0]:
                print(checks[1])
                return True
            elif checks[1] == "Passed the pipe" and not self.pointGiven:
                # give point
                self.pointGiven = True


class PipesRenderer:
    """
    The pipes renderer class.

    Args:
        parent (tkinter.Frame): The parent widget.
        canvas (tkinter.Canvas): The canvas to draw the pipes on.

    """

    def __init__(self, parent, canvas):
        self.parent = parent
        self.canvas = canvas

        self.pipeSpeed = 3
        self.pipeWidth = 50
        self.pipeGap = 150
        self.pipeList = []

    def createNewPipe(self, xOffset):
        """
        Create a new pipe.

        Args:
            xOffset (int): The x-coordinate offset of the pipe.

        """
        print("Creating new pipe")
        pipe = Pipe(
            self.parent,
            self.canvas,
            xOffset,
            self.pipeGap,
            self.pipeWidth,
        )
        self.pipeList.append(pipe)

    def checkPipesCollision(self, birdRenderer):
        """
        Check for collision between the bird and the pipes.

        Args:
            birdRenderer (birdRenderer): The bird renderer object.

        """
        bird_coords = birdRenderer.getCoords()
        for pipe in self.pipeList:
            if not pipe.pointGiven:
                if pipe.checkPipeCollision(bird_coords):
                    self.parent.gameIsRunning = False


class BirdRenderer:
    """
    The bird renderer class.

    Args:
        parent (tkinter.Frame): The parent widget.
        canvas (tkinter.Canvas): The canvas to draw the bird on.

    """

    def __init__(self, parent, canvas):
        self.parent = parent
        self.canvas = canvas

        self.width = 64
        self.height = 64

        self.birdStates = {
            "up": tk.PhotoImage(file="assets/sprites_64/totoUp.png"),
            "down": tk.PhotoImage(file="assets/sprites_64/totoDown.png"),
            "falling": tk.PhotoImage(file="assets/sprites_64/totoFalling.png"),
        }

        self.bird = self.canvas.create_image(
            50,
            self.parent.windowHeight / 2,
            image=self.birdStates["up"],
            anchor="nw",
        )

        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.canvas.tag_bind(self.bird, "<ButtonPress-1>", self.startDrag)
        self.canvas.tag_bind(self.bird, "<B1-Motion>", self.drag)

    def startDrag(self, event):
        """
        Start dragging the bird.

        Args:
            event (tkinter.Event): The event object.

        """
        theItem = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = theItem
        self.drag_data["x"] = event.x - self.canvas.coords(theItem)[0]
        self.drag_data["y"] = event.y - self.canvas.coords(theItem)[1]

    def drag(self, event):
        """
        Drag the bird.

        Args:
            event (tkinter.Event): The event object.

        """
        self.canvas.coords(
            self.drag_data["item"],
            event.x - self.drag_data["x"],
            event.y - self.drag_data["y"],
        )

    def getCoords(self):
        """
        Get the coordinates of the bird.

        Returns:
            list: The coordinates of the bird.

        """
        birdCoords = self.canvas.coords(self.bird)
        if len(birdCoords) == 2:
            birdCoords += [
                birdCoords[0] + self.width,
                birdCoords[1] + self.height,
            ]
        return birdCoords


class GameRuntime:
    """
    The game runtime class.

    Args:
        parent (tkinter.Frame): The parent widget.
        canvas (tkinter.Canvas): The canvas to draw the game on.
        **kwargs: Arbitrary keyword arguments.

    """

    def __init__(self, parent, canvas, **kwargs):
        self.parent = parent
        self.canvas = canvas

        self.windowHeight = kwargs["windowHeight"]
        self.windowWidth = kwargs["windowWidth"]

        self.gameIsRunning = True

        self.birdRenderer = BirdRenderer(
            self,
            self.canvas,
        )

        self.pipesRenderer = PipesRenderer(
            self,
            self.canvas,
        )

        self.pipesRenderer.createNewPipe(200)
        self.pipesRenderer.createNewPipe(400)
        self.pipesRenderer.createNewPipe(600)

    def gameLoop(self):
        """
        The main game loop.

        """
        self.pipesRenderer.checkPipesCollision(self.birdRenderer)
        if self.gameIsRunning:
            root.after(20, self.gameLoop)


if __name__ == "__main__":
    gameWindowWidth = 800
    gameWindowHeight = 800

    root = tk.Tk()
    root.title("Floppy Totoro")
    newGameWindow = GameWindow(root)
    newGameWindow.pack(side="top", fill="both", expand=True)
    game = GameRuntime(
        newGameWindow,
        newGameWindow.gameBackground,
        windowHeight=gameWindowHeight,
        windowWidth=gameWindowWidth,
    )
    myDebugInfo = DebugInfo(newGameWindow)
    game.gameLoop()
    root.mainloop()
