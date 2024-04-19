import tkinter as tk
import random


def checkCoordCollision(hitboxCoord, coordsToCheckAgainstList):
    result = []
    for coordToCheckAgainst in coordsToCheckAgainstList:
        if (
            hitboxCoord[2] > coordToCheckAgainst[0]
            and hitboxCoord[0] < coordToCheckAgainst[2]
            and hitboxCoord[3] > coordToCheckAgainst[1]
            and hitboxCoord[1] < coordToCheckAgainst[3]
        ):
            result.append([True, "Hit the object"])
        elif hitboxCoord[3] > 800:  # Change 800 to dynamic value
            result.append([True, "Hit the bottom of the screen"])
        elif hitboxCoord[1] < 0:
            result.append([True, "Hit the top of the screen"])
        elif hitboxCoord[0] > coordToCheckAgainst[2]:
            result.append([False, "Passed the pipe"])
        else:
            result.append([False, "No collision"])
    return result


class gameWindow(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root  # Not used right now
        self.windowWidth = 800
        self.windowHeight = 800

        self.gameBackground = gameBackground(
            self, width=self.windowWidth, height=self.windowHeight, bg="skyblue"
        )
        self.gameBackground.pack()


class gameBackground(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # self.config(bg="yellow")


class Pipe:
    def __init__(self, canvas, window_width, window_height, pipe_gap, pipe_width):
        self.canvas = canvas

        self.window_width = window_width
        self.window_height = window_height

        self.pipe_gap = pipe_gap
        self.pipe_width = pipe_width

        self.pointGiven = False

        self.top_y = random.randint(50, self.window_height - self.pipe_gap - 50)
        self.bottom_y = self.top_y + self.pipe_gap

        self.top = self.canvas.create_rectangle(
            self.window_width,
            0,
            self.window_width + self.pipe_width,
            self.top_y,
            fill="green",
        )
        self.bottom = self.canvas.create_rectangle(
            self.window_width,
            self.bottom_y,
            self.window_width + self.pipe_width,
            self.window_height,
            fill="green",
        )
        self.updateCurrentCoords()

    def updateCurrentCoords(self):
        self.top_coords = self.canvas.coords(self.top)
        self.bottom_coords = self.canvas.coords(self.bottom)

    def movePipe(self, pipe_speed):
        self.canvas.move(self.top, -pipe_speed, 0)
        self.canvas.move(self.bottom, -pipe_speed, 0)
        self.updateCurrentCoords()
        # print(f"Coords: {self.top_coords} ::: {self.bottom_coords}")

    def checkPipeCollision(self, birdCoords):
        for checks in checkCoordCollision(
            birdCoords, [self.top_coords, self.bottom_coords]
        ):
            if checks[0]:
                print(checks[1])
                return True
            elif checks[1] == "Passed the pipe" and not self.pointGiven:
                # give point
                self.pointGiven = True


class pipesRenderer:
    def __init__(self, parent, canvas, *args, **kwargs):
        self.parent = parent
        self.canvas = canvas
        self.windowHeight = kwargs["windowHeight"]
        self.windowWidth = kwargs["windowWidth"]

        print(f"Window Height: {self.windowHeight}")
        print(f"Window Width: {self.windowWidth}")
        print(f"2Window Height: {self.parent.windowHeight}")
        print(f"2Window Width: {self.parent.windowWidth}")

        self.pipeSpeed = 3
        self.pipeWidth = 50
        self.pipeGap = 150
        self.pipeList = []

        self.createNewPipe()

    def createNewPipe(self):
        print("Creating new pipe")
        pipe = Pipe(
            self.canvas,
            self.windowWidth,
            self.windowHeight,
            self.pipeGap,
            self.pipeWidth,
        )
        self.pipeList.append(pipe)

    def updatePipes(self):
        for pipe in self.pipeList:
            pipe.movePipe(self.pipeSpeed)
            if self.canvas.coords(pipe.top)[2] < 0:
                self.canvas.delete(pipe.top)
                self.canvas.delete(pipe.bottom)
                self.pipeList.remove(pipe)
                self.createNewPipe()

    def checkPipesCollision(self, birdRenderer):
        bird_coords = birdRenderer.getCoords()
        for pipe in self.pipeList:
            if not pipe.pointGiven:
                if pipe.checkPipeCollision(bird_coords):
                    self.parent.gameIsRunning = False


class birdRenderer:
    def __init__(self, parent, canvas, *args, **kwargs):
        self.parent = parent
        self.canvas = canvas
        self.windowHeight = kwargs["windowHeight"]
        self.windowWidth = kwargs["windowWidth"]

        self.width = 64
        self.height = 64

        self.birdStates = {
            "up": tk.PhotoImage(file="assets/sprites_64/totoUp.png"),
            "down": tk.PhotoImage(file="assets/sprites_64/totoDown.png"),
            "falling": tk.PhotoImage(file="assets/sprites_64/totoFalling.png"),
        }

        self.birdYVelocity = 0
        self.jumpStrength = 6
        self.gravity = 0.25

        self.bird = self.canvas.create_image(
            50, self.windowHeight / 2, image=self.birdStates["up"], anchor="nw"
        )

        root.bind("<space>", lambda event: self.jump())

    def reskinBird(self, state):
        self.canvas.itemconfig(self.bird, image=self.birdStates[state])

    def jump(self):
        self.birdYVelocity = -self.jumpStrength

    def updateBird(self):
        self.birdYVelocity += self.gravity
        self.canvas.move(self.bird, 0, self.birdYVelocity)
        if self.birdYVelocity < 0:
            self.reskinBird("up")
        else:
            self.reskinBird("down")

    def getCoords(self):
        birdCoords = self.canvas.coords(self.bird)
        if len(birdCoords) == 2:
            birdCoords += [
                birdCoords[0] + self.width,
                birdCoords[1] + self.height,
            ]
        return birdCoords


class gameRuntime:
    def __init__(self, parent, canvas, **kwargs):
        self.parent = parent  # gameWindow : Not used right now
        print(f"aWindow Height: {self.parent.winfo_reqheight()}")
        print(f"aWindow Width: {self.parent.winfo_reqwidth()}")
        self.canvas = canvas
        self.windowHeight = kwargs["windowHeight"]
        self.windowWidth = kwargs["windowWidth"]

        self.gameIsRunning = True

        self.birdRenderer = birdRenderer(
            self,
            self.canvas,
            windowHeight=self.windowHeight,
            windowWidth=self.windowWidth,
        )

        self.pipesRenderer = pipesRenderer(
            self,
            self.canvas,
            windowHeight=self.windowHeight,
            windowWidth=self.windowWidth,
        )

    def gameLoop(self):
        self.birdRenderer.updateBird()
        self.pipesRenderer.updatePipes()
        self.pipesRenderer.checkPipesCollision(self.birdRenderer)
        if self.gameIsRunning:
            root.after(20, self.gameLoop)


if __name__ == "__main__":
    gameWindowWidth = 800
    gameWindowHeight = 800

    root = tk.Tk()
    root.title("Floppy Totoro")
    newGameWindow = gameWindow(root)
    newGameWindow.pack(side="top", fill="both", expand=True)
    game = gameRuntime(
        newGameWindow,
        newGameWindow.gameBackground,
        windowHeight=gameWindowHeight,
        windowWidth=gameWindowWidth,
    )
    game.gameLoop()
    root.mainloop()
