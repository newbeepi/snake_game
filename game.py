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
    x: int
    y: int
    type_: str # snake body type(body, head or tail)
    state: str # state(up, left, down, right)
    sprite: Image
    last_tail_place: tuple[int, int] 

    # Creating Snake Box (body by default)
    def __init__(self, x: int, y: int, type_="body", state="") -> None:
        self.x = x
        self.y = y
        self.type_ = type_
        self.state = state
    
    def update_sprite(self) -> None:
        if self.type_ == "body":
            self.sprite = Image.open(BASE_SPRITE_PATH + "body.png")
        else:
            self.sprite = Image.open(BASE_SPRITE_PATH + f"{self.type_}_{self.state[0]}.png")
        
        if self.type_ == "tail":
            self.last_tail_place = (self.x, self.y)
    
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

    def draw(self, field: Image) -> None:
        self.update_sprite()
        field.paste(self.sprite, ((MAX_X_SIZE // 2 + self.x) * 36, (MAX_Y_SIZE // 2 + self.y) * 36))

class Snake:
    snake_boxes = []
    history = []
    # Creating Snake
    def __init__(self) -> None:
        head = SnakeBox(0, 0, "head", "left")
        body = [SnakeBox(1, 0), SnakeBox(2, 0), SnakeBox(3, 0)]
        tail = SnakeBox(4, 0, "tail", "left")
        
        self.snake_boxes.append(head)
        self.snake_boxes.extend(body)
        self.snake_boxes.append(tail)
        self.history = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    
    def draw_snake(self, field: Image) -> None:
        for snake_box in self.snake_boxes:
            snake_box.draw(field)
    
    def move(self, direction: str) -> None:
        new_head_position = self.snake_boxes[0].move_dir(direction)
        self.history.insert(0, new_head_position)
        for segment_num in range(1, len(self.snake_boxes)):
            self.snake_boxes[segment_num].move_coordinates(*self.history[segment_num])
        self.snake_boxes[-1].move_coordinates(*self.history[-2])
        self.history.pop()


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
    
    def move(self, direction: str) -> None:
        directions = {
            "w": "up",
            "d": "right",
            "s": "down",
            "a": "left"
        }
        self.snake.move(directions.get(direction, "skip"))
    
    def check_move(self):
        pressed = list(map(keyboard.is_pressed, ("a", "s", "w", "d")))
        if any(pressed):
            pressed_key = ""
            if keyboard.is_pressed("a"):
                pressed_key = "a"
            elif keyboard.is_pressed("w"):
                pressed_key = "w"
            elif keyboard.is_pressed("s"):
                pressed_key = "s"
            elif keyboard.is_pressed("d"):
                pressed_key = "d"
            self.move(pressed_key)
        else:
            self.move("skip")
        self.root.after(1000 // SPEED, self.check_move)

    def play(self) -> None:
        self.root.after(0, self.draw_fields)
        self.root.after(1000 // SPEED, self.check_move)
        self.root.mainloop()

if __name__ == "__main__":

    game: Game = Game()

    game.play()