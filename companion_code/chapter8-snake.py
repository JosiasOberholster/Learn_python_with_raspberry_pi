import minecraft
import pygame
import sys
import time
import random

from pygame.locals import *

mc = minecraft.Minecraft.create()
pygame.init()

#blank world
print("Resetting world")
mc.setBlocks(-100,-1,-100, 100, 0, 100, 2)
mc.setBlocks(-100,1,-100, 100, 100, 100, 0)
mc.player.setPos(0,2,0)

# create control window
display = pygame.display.set_mode((200,200))

#draw maze
print("drawing maze")
height = 10

start_x = 0
start_z = 0

difficulty = 0.5
apple_freq = 2

picture = [["R", "R", "R", "R", "R", "R", "R", "R", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "-", "-", "-", "-", "-", "-", "-", "R"],
           ["R", "R", "R", "R", "R", "R", "R", "R", "R"]]


if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        picture = f.readlines()

posn_z = start_z
for line in picture:
    posn_x = start_x
    for block in line:
        x = height
        y = posn_x
        z = posn_z

        if block == "R":
            mc.setBlock(x,y,z,246)

        posn_x = posn_x + 1
    posn_z = posn_z + 1


snake = [(int((posn_z - start_z)/2),int((posn_x - start_x)/2))]
movement = [-1,0]

finished = False

grow_in = []
apple_in = apple_freq


while not finished:
    for event in pygame.event.get():
        if event.type == QUIT:
            finished = True

#note -- you have to keep the key pressed down until it's moved
    key_state = pygame.key.get_pressed()
    if key_state[K_LEFT]:
        movement = [-1,0]
    if key_state[K_RIGHT]:
        movement = [1,0]
    if key_state[K_UP]:
        movement = [0,1]
    if key_state[K_DOWN]:
        movement = [0,-1]

    next_position = (height, snake[0][1] + movement[1], snake[0][0] + movement[0])
    next_block = mc.getBlock(next_position[0],next_position[1], next_position[2])

    if next_block == 246 or next_block == 22:
        finished = True

    if next_block == 18:
        grow_in.append(len(snake))
        apple_in = apple_freq

    snake.insert(0, (next_position[2], next_position[1]))
    for block in snake:
        mc.setBlock(height, block[1], block[0], 22)

    if 0 not in grow_in:
        remove_block = snake.pop()
        mc.setBlock(height, remove_block[1], remove_block[0], 0)

    grow_in2 = []
    for number in grow_in:
        if number > -1:
            grow_in2.append(number - 1)
    grow_in = grow_in2

    if apple_in == 0:
        apple_y = random.randint(1,int(posn_x - start_x)-1)
        apple_x = random.randint(1,int(posn_z - start_z)-1)
        while mc.getBlock(height, apple_y, apple_x) != 0:
            apple_x = random.randint(1,int(posn_z - start_z)-1)
            apple_y = random.randint(1,int(posn_x - start_x)-1)
        mc.setBlock(height, apple_y, apple_x, 18)


    apple_in = apple_in - 1 


    time.sleep(difficulty)

mc.postToChat("Game Over")

 