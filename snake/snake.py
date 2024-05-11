from __future__ import annotations
from typing import List
import random
import math

# Constants for directions, block size, and screen dimensions
from config import block_size, bg_width, bg_height, UP, RIGHT, DOWN, LEFT

# Colors (could be defined in a separate config module)
green = (0, 128, 0)
red = (0, 0, 255)

class Snake:
    def __init__(self, color=green, hunger=200):
        self.head = [10 * block_size, 5 * block_size]
        self.color = color
        self.hunger = hunger
        self.body = [self.head[:], [9 * block_size, 5 * block_size]]
        self.direction = RIGHT
        self.size = 2

    def change_dir(self, direc: str):
        opposite_directions = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}
        if self.direction != opposite_directions[direc]:
            self.direction = direc

    def move(self):
        movement = {RIGHT: [block_size, 0], LEFT: [-block_size, 0], UP: [0, -block_size], DOWN: [0, block_size]}
        move = movement[self.direction]
        self.head = [self.head[0] + move[0], self.head[1] + move[1]]
        self.body.insert(0, self.head[:])
        self.body.pop()

    def add_to_tail(self):
        self.body.append(self.body[-1][:])
        self.size += 1

    def get_body(self) -> List[List[int]]:
        return self.body

class Food:
    def __init__(self, color=red):
        self.color = color
        self.spawn_new_food()

    def spawn_new_food(self):
        self.position = [random.randint(0, (bg_width // block_size) - 1) * block_size,
                         random.randint(0, (bg_height // block_size) - 1) * block_size]
        self.state = True

    def get_cords(self):
        return self.position

def check_collision(point1: List[int], point2: List[int]):
    return point1 == point2

def wall_collision(snake: Snake) -> bool:
    x, y = snake.head
    return x < 0 or x >= bg_width or y < 0 or y >= bg_height

def body_collision(snake: Snake) -> bool:
    head = snake.head
    return head in snake.body[1:]

def senses(snake: Snake, apple: Food) -> list:
    head_pos = snake.head
    apple_pos = apple.get_cords()
    angle = math.degrees(math.atan2(-(apple_pos[1] - head_pos[1]), apple_pos[0] - head_pos[0]))

    obstacles = [check_block(snake, [head_pos[0] + dx * block_size, head_pos[1] + dy * block_size]) for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]]
    return [angle / 180] + obstacles

def check_block(snake: Snake, block: List[int]):
    if block in snake.body or block[0] < 0 or block[0] >= bg_width or block[1] < 0 or block[1] >= bg_height:
        return 1
    return 0
