import pygame
import sys
from pygame.locals import *
from random import randint

class Player(pygame.sprite.Sprite):
    '''The class that holds the main player, and controls how they jump. nb. The player doens't move left or right, the world moves around them'''
    def __init__(self, start_x, start_y, width, height):
        pass

    def move_y(self):
        '''this calculates the y-axis movement for the player in the 
        current speed'''
        pass

    def jump(self, speed):
        '''This sets the player to jump, but it only can if its feet are on the floor'''
        pass

class World():
    '''This will hold the platforms and the goal. 
    nb. In this game, the world moves left and right rather than the player'''
    def __init__(self, level, block_size, colour_platform, colour_goals):
        pass

    def move(self, dist):
        '''move the world dist pixels right (a negative dist means left)'''
        pass

    def collided_get_y(self, player_rect):
        '''get the y value of the platform the player is currently on'''
        pass

    def at_goal(self, player_rect):
        '''return True if the player is currently in contact with the goal. False otherwise'''
        pass

    def update(self, screen):
        '''draw all the rectangles onto the screen'''
        pass

class Doom():
    '''this class holds all the things that can kill the player'''
    def __init__(self, fireball_num, pit_depth, colour):
        pass

    def move(self, dist):
        '''move everything right dist pixels (negative dist means left)'''
        pass

    def update(self, screen):
        '''move fireballs down, and draw everything on the screen'''
        pass

    def collided(self, player_rect):
        '''check if the player is currently in contact with any of the doom.
        nb. shrink the rectangle for the fireballs to make it fairer'''
        pass

class Fireball(pygame.sprite.Sprite):
    '''this class holds the fireballs that fall from the sky'''
    def __init__(self):
        pass

    def reset(self):
        '''re-generate the fireball a random distance along the screen and give them a random speed'''
        pass

    def move_x(self, dist):
        '''move the fireballs dist pixels to the right 
        (negative dist means left)'''
        pass

    def move_y(self):
        '''move the fireball the appropriate distance down the screen
        nb. fireballs don't accellerate with gravity, but have a random speed. if the fireball has reached the bottom of the screen, 
        regenerate it'''
        pass

    def update(self, screen, colour):
        '''draw the fireball onto the screen'''
        pass
#options
#initialise pygame.mixer
#initialise pygame
#load level
#initialise variables
finished = False
#setup the background
while not finished:
    pass
    #blank screen   
    #check events
    #check which keys are held      
    #move the player with gravity
    #render the frame
    #update the display
    #check if the player is dead
    #check if the player has completed the level
    #set the speed