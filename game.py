from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import keyboard


MAX_X_SIZE = 40 # Maximum size of Field
MAX_Y_SIZE = 20
BOX_SIZE = 36 # Sprite size of each box
BASE_SPRITE_PATH = "icons/" # Base path to all sprites
SPEED = 2 # 2 tiles per sec

class Box:
    x: int # x-coordinate of box
    y: int # y-coordinate of box
    can_pass: bool = True # can snake pass the box?
    sprite_path: str = BASE_SPRITE_PATH + "field.png" # path to sprite
    sprite: Image

    def __init__(self, x:int, y:int) -> None:
        if x == 0 or y == 0 or x == MAX_X_SIZE-1 or y == MAX_Y_SIZE-1: # if box is on border - snake shouldn't pass it
            self.can_pass = False
            self.sprite_path = BASE_SPRITE_PATH + "fieldzone.png" # changing sprite path
        self.x = x
        self.y = y
        self.sprite = Image.open(self.sprite_path)


class SnakeBox:
    x: int  # Relative coordinates from center
    y: int
    type_: str # snake body type(body, head or tail)
    state: str # state(up, left, down, right)
    sprite: Image   # image sprite
    last_tail_place: tuple[int, int] 

    # Creating Snake Box (body by default)
    def __init__(self, x: int, y: int, type_="body", state="") -> None:
        self.x = x
        self.y = y
        self.type_ = type_
        self.state = state
    
    # Updates image sprite
    def update_sprite(self) -> None:
        if self.type_ == "body":
            self.sprite = Image.open(BASE_SPRITE_PATH + "body.png")
        else:
            self.sprite = Image.open(BASE_SPRITE_PATH + f"{self.type_}_{self.state[0]}.png")
        
        if self.type_ == "tail":
            self.last_tail_place = (self.x, self.y)
    
    # Move snake box in specific direction
    def move_dir(self, direction: str) -> tuple[int, int]:
        dx = 0
        dy = 0
        if direction == "skip":
            direction = self.state
        if direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        elif direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        self.x += dx
        self.y += dy
        self.state = direction
        return self.x, self.y

    # Move snake box to specific coordinates
    def move_coordinates(self, x: int, y: int) -> None:
        if x < self.x:
            self.state = "left"
        elif y < self.y:
            self.state = "up"
        elif x > self.x:
            self.state = "right"
        elif y > self.y:
            self.state = "down"
        self.x = x
        self.y = y

    # Draw snake box
    def draw(self, field: Image) -> None:
        self.update_sprite() # Updating sprite
        field.paste(self.sprite, ((MAX_X_SIZE // 2 + self.x) * 36, (MAX_Y_SIZE // 2 + self.y) * 36)) # As coordinates are relative we should divide them by 2. 36 is a block size

class Snake:
    snake_boxes = [] # All snake body(head, body and tail)
    history = [] # Snake moving history
    direction: str

    # Creating Snake
    def __init__(self) -> None:
        head = SnakeBox(0, 0, "head", "left") # Creating snake head in initial position(0, 0)
        body = [SnakeBox(1, 0), SnakeBox(2, 0), SnakeBox(3, 0)] # Creating snake body in initial positions
        tail = SnakeBox(4, 0, "tail", "left") # Creating Snake tail in initial position
        self.direction = "left"
        # Put it all together
        self.snake_boxes.append(head)
        self.snake_boxes.extend(body)
        self.snake_boxes.append(tail)

        # Update history
        self.history = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    
    # Draw all snake sprites on screen
    def draw_snake(self, field: Image) -> None:
        for snake_box in self.snake_boxes:
            snake_box.draw(field)
    
    def move(self) -> None:
        # Snake moving logic
        # First step - we are moving snake head in specific direction and insert new position in the start of our history list
        new_head_position = self.snake_boxes[0].move_dir(self.direction)
        self.history.insert(0, new_head_position)

        # Second step - for every body tile we get the next body tile previous position and move it
        for segment_num in range(1, len(self.snake_boxes)):
            self.snake_boxes[segment_num].move_coordinates(*self.history[segment_num])
        
        self.snake_boxes[-1].move_coordinates(*self.history[-2])
        self.history.pop()
    
    def set_direction(self, direction: str):
        possible_directions = {
            "left": ["up", "down"],
            "right": ["up", "down"],
            "up": ["left", "right"],
            "down": ["left", "right"]
        }
        if direction in possible_directions[self.direction]:
            self.direction = direction


class Game:
    boxes: list[Box] = []
    field: Image
    snake = Snake()

    def __init__(self) -> None:
        self.root = tk.Tk()
        for x in range(MAX_X_SIZE):
            for y in range(MAX_Y_SIZE):
                self.boxes.append(Box(x, y))
        self.field = Image.new("RGB", (MAX_X_SIZE * BOX_SIZE, MAX_Y_SIZE * BOX_SIZE), (0, 0, 0))
        self.screen = tk.Label(self.root, image=ImageTk.PhotoImage(self.field))
        self.screen.pack()

    def draw_fields(self) -> None:
        for box in self.boxes:
            self.field.paste(box.sprite, (box.x * BOX_SIZE, box.y * BOX_SIZE))
        self.snake.draw_snake(self.field)
        new_img = ImageTk.PhotoImage(self.field)
        self.screen.config(image=new_img)
        self.screen.image = new_img
        self.root.after(100, self.draw_fields)
    
    def move(self) -> None:
        self.snake.move()
        self.root.after(1000 // SPEED, self.move)

    def set_direction(self, event) -> None:
        pressed_key = event.keysym
        directions = {
            "w": "up",
            "d": "right",
            "s": "down",
            "a": "left"
        }
        if pressed_key in ['a', 's', 'd', 'w']:
            self.snake.set_direction(directions[pressed_key])

    def play(self) -> None:
        self.root.after(0, self.draw_fields)
        self.root.after(1000 // SPEED, self.move)
        self.root.bind("<KeyPress>", self.set_direction)
        self.root.mainloop()

if __name__ == "__main__":

    game: Game = Game()

    game.play()
