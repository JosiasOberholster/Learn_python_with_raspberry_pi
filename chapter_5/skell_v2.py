import pygame
import sys
from pygame.locals import *
from random import randint

class Landing_Page():
    #The class that holds the details to allow the user to start a game, 
    #change the level difficulty and quit the game

    def __init__(self, select_start_number, select_min_number, select_max_number):
        self.current_selected_number = select_start_number
        self.min_number = select_min_number
        self.max_number = select_max_number

    def Select_Options(self, currentKeyValue):
        #Function to see what the current option is and navigate to the correct one
        if currentKeyValue == 'down':
            if self.current_selected_number != self.max_number:
                self.current_selected_number += 1
        if currentKeyValue == 'up':
            if self.current_selected_number != self.min_number:
                self.current_selected_number -= 1
        return self.current_selected_number

    def Update_Options(self, new_selected_option):
        #This will update the current selected option to the new one
        # if new_selected_option != self.current_selected_number:
        if new_selected_option == 1:
            screen.fill((0, 0, 0))
            screen.blit(landing_page_image, (0, 0))
            screen.blit(pygame.image.load(landing_page_logo), (190, 45))
            screen.blit(pygame.image.load(landing_page_start_selected), (216, 166))
            screen.blit(pygame.image.load(landing_page_difficulty), (216, 218))
            screen.blit(pygame.image.load(landing_page_quit), (216, 271))
        elif new_selected_option == 2:
            screen.fill((0, 0, 0))
            screen.blit(landing_page_image, (0, 0))
            screen.blit(pygame.image.load(landing_page_logo), (190, 45))
            screen.blit(pygame.image.load(landing_page_start), (216, 166))
            screen.blit(pygame.image.load(landing_page_difficulty_selected), (216, 218))
            screen.blit(pygame.image.load(landing_page_quit), (216, 271))
        elif new_selected_option == 3:
            screen.fill((0, 0, 0))
            screen.blit(landing_page_image, (0, 0))
            screen.blit(pygame.image.load(landing_page_logo), (190, 45))
            screen.blit(pygame.image.load(landing_page_start), (216, 166))
            screen.blit(pygame.image.load(landing_page_difficulty), (216, 218))
            screen.blit(pygame.image.load(landing_page_quit_selected), (216, 271))
        pygame.display.update()


class Player(pygame.sprite.Sprite):
    #The class that holds the main player, and controls
    #how they jump. nb. The player doesn't move left or right,
    #the world moves around them

    def __init__(self, start_x, start_y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed_y = 0
        self.base = pygame.Rect(start_x, start_y + height, width, 2)
        self.sound = pygame.mixer.Sound(jump_sound)

    def move_y(self):
        #This calculates the y-axis movement for the player
        #in the current speed
        #self.rect.y = self.rect.y + 1
        collided_y = world.collided_get_y(self.base)
        if self.speed_y <= 0 or collided_y < 0:
            self.rect.y = self.rect.y + self.speed_y
            self.speed_y = self.speed_y + gravity
        if collided_y > 0 and self.speed_y > 0:
            self.rect.y = collided_y
        self.base.y = self.rect.y + self.rect.height

    def jump(self, speed):
        #This will hold the platform and the goal.
        #nb. In this game, the world moves left and right rather
        #than the player
        if world.collided_get_y(self.base) > 0:
            self.speed_y = speed
            self.sound.play()

class World():
    #This will hold the platform and the goal.
    #nb. In this game, the world moves left and right rather 
    #than the player

    def __init__(self, level, block_size, colour_platform, colour_goals):
        self.platforms = []
        self.goals = []
        self.posn_y = 0
        self.colour = colour_platform
        self.colour_goals = colour_goals
        self.block_sizee = block_size

        for line in level:
            self.posn_x = 0
            for block in line:
                if block == "-":
                    self.platforms.append(pygame.Rect(self.posn_x, self.posn_y, block_size, block_size))
                if block == "G":
                    self.goals.append(pygame.Rect(self.posn_x, self.posn_y, block_size, block_size))
                self.posn_x = self.posn_x + block_size
            self.posn_y = self.posn_y + block_size


    def move(self, dist):
        #Move the world dist pixels right (a negative dist
        #means left)
        for block in self.platforms + self.goals:
            block.move_ip(dist, 0)

    def collided_get_y(self, player_rect):
        #Get the y value of the platform the player is
        #currently on
        return_y = -1
        for block in self.platforms:
            if block.colliderect(player_rect):
                return_y = block.y - block.height + 1
        return return_y

    def at_goal(self, player_rect):
        #Return True if the player is currently in contact
        #with the goal. Flase otherwise
        for block in self.goals:
            if block.colliderect(player_rect):
                return True
        return False

    def update(self, screen):
        #Draw all the rectangles onto the screen
        for block in self.platforms:
            pygame.draw.rect(screen, self.colour, block, 0)
        for block in self.goals:
            pygame.draw.rect(screen, self.colour_goals, block, 0)

class Doom():
    #This class holds all the things that can kill the player
    
    def __init__(self, fireball_num, pit_depth, colour):
        self.base = pygame.Rect(0, screen_y - pit_depth, screen_x, pit_depth)
        self.colour = colour
        self.fireballs = []
        for i in range(0, fireball_num):
            self.fireballs.append(Fireball())
        self.fireball_plain = pygame.sprite.RenderPlain(self.fireballs)

    def move(self, dist):
        #Move everyting right dist pixels (negative dist means left)
        for fireball in self.fireballs:
            fireball.move_x(dist)

    def update(self, screen):
        #Move fireballs down, and draw everything on the screen
        for fireball in self.fireballs:
            fireball.move_y()
        self.fireball_plain.draw(screen)
        pygame.draw.rect(screen, self.colour, self.base, 0)

    def collided(self, player_rect):
        #Check if the player is currently in contact with
        #any of the doom.
        #nb. Shrink the rectangle for the fireballs to make it fairer
        for fireball in self.fireballs:
            if fireball.rect.colliderect(player_rect):
                hit_box = fireball.rect.inflate(-int(fireball_size/2), -int(fireball_size/2))
                if hit_box.colliderect(player_rect):
                    return True
        return self.base.colliderect(player_rect)

class Fireball(pygame.sprite.Sprite):
    #This class holds the fireballs that fall from the sky

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(fireball_image), (fireball_size, fireball_size))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        #Re-generate the fireball a random distance along
        #the screen and give them a random speed
        self.y = 0
        self.speed_y = randint(fireball_low_speed, fireball_high_speed)
        #Set closest left side distance that the fireball will start 
        self.x = randint(80, screen_x)
        self.rect.topleft = self.x, self.y

    def move_x(self, dist):
        #Move the fireballs dist pixels to the right
        #(negative dist means left)
        self.rect.move_ip(dist, 0)
        if self.rect.x < -50 or self.rect.x > screen_x:
            self.reset()

    def move_y(self):
        #Move the fireball the appropriate distance down
        #the screen
        #nb. fireballs don't accellerate with gravity, but
        #have a random speed. If the fireball has reached the
        #bottom of the screen, regerate it
        self.rect.move_ip(0, self.speed_y)
        if self.rect.y > screen_y:
            self.reset()

    def update(self, screen, colour):
        '''draw the fireball onto the screen'''
        pass

#options
screen_x = 600
screen_y = 400
game_name = "Skell Platformer Game"
player_spawn_x = 50
player_spawn_y = 200
player_image = "sprites/lidia.png"
level = [
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "                              ",
    "          ---                G",
    "     -- --    ---       ------",
    " -- -            -------      "]
platform_colour = (100, 100, 100)
goal_colour = (0, 0, 255)
gravity = 1
jump_speed = -10
doom_colour = (255, 0, 0)
fireball_size = 30
fireball_number = 10
fireball_low_speed = 1
fireball_high_speed = 3
fireball_image = "sprites/flame.png"
jump_sound = "sound/qubodup-cfork-ccby3-jump.ogg"
background_image = "images/background.png"
landing_page_background = "images/LandingPageBackground.png"
landing_page_logo = "images/LandingPageLogo.png"
landing_page_start = "images/LandingPageStart.png"
landing_page_start_selected = "images/LandingPageStartSelected.png"
landing_page_difficulty = "images/LandingPageDifficulty.png"
landing_page_difficulty_selected = "images/LandingPageDifficultySelected.png"
landing_page_quit = "images/LandingPageQuit.png"
landing_page_quit_selected = "images/LandingPageQuitSelected.png"
landing_page_start_number = 1
landing_page_min_selection_number = 1
landing_page_max_selection_number = 3

#initialise pygame.mixer
pygame.mixer.pre_init(44100, -16, 8, 2048)
pygame.mixer.init()

#initialise pygame
pygame.init()
window = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption(game_name)
screen = pygame.display.get_surface()

#load level
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        level = f.readlines()

#initialise variables
start = False
finished = False
complete_loading = False
clock = pygame.time.Clock()
player = Player(player_spawn_x, player_spawn_y, 20, 30)
player_plain = pygame.sprite.RenderPlain(player)
world = World(level, 30, platform_colour, goal_colour)
doom = Doom(fireball_number, 10, doom_colour)
landing_page = Landing_Page(landing_page_start_number, landing_page_min_selection_number, landing_page_max_selection_number)

#set the speed
clock.tick(20)

#setup the landing page
landing_page_image = pygame.transform.scale(pygame.image.load(landing_page_background), (screen_x, screen_y)).convert()

#setup the background
background = pygame.transform.scale(pygame.image.load(background_image), (screen_x, screen_y))
bg_1_x = -100
bg_2_x = screen_x - 100

while not finished:
    #render the frame
    if not complete_loading:
        screen.fill((0, 0, 0))
        screen.blit(landing_page_image, (0, 0))
        screen.blit(pygame.image.load(landing_page_logo), (190, 45))
        screen.blit(pygame.image.load(landing_page_start_selected), (216, 166))
        screen.blit(pygame.image.load(landing_page_difficulty), (216, 218))
        screen.blit(pygame.image.load(landing_page_quit), (216, 271))
        complete_loading = True

    #check events
    for event in pygame.event.get():
        if event.type == QUIT:
            finished = True
        if event.type == KEYDOWN:
            if event.key == pygame.K_DOWN:
                new_option = landing_page.Select_Options("down")
                landing_page.Update_Options(new_option)    
            if event.key == pygame.K_UP:
                new_option = landing_page.Select_Options('up')
                landing_page.Update_Options(new_option)
            if event.key == pygame.K_SPACE:
                if landing_page.current_selected_number == 1:
                    start = True
                elif landing_page.current_selected_number == 2:
                    print('difficulty')
                elif landing_page.current_selected_number == 3:
                    print('quit')
    
    #update the display
    pygame.display.update()
    
    while start:
        #black screen
        screen.fill((0, 0, 0))

        #check events
        for event in pygame.event.get():
            if event.type == QUIT:
                finished = True

        #check which keys are held
        key_state = pygame.key.get_pressed()
        if key_state[K_LEFT]:
            world.move(2)
            doom.move(2)
            bg_1_x = bg_1_x + 1
            bg_2_x = bg_2_x + 1
            if bg_1_x > screen_x:
                bg_1_x = -screen_x
            if bg_2_x > screen_x:
                bg_2_x = -screen_x
        elif key_state[K_RIGHT]:
            world.move(-2)
            doom.move(-2)
            bg_1_x = bg_1_x - 1
            bg_2_x = bg_2_x - 1
            if bg_1_x < -screen_x:
                bg_1_x = screen_x
            if bg_2_x < -screen_x:
                bg_2_x = screen_x
        if key_state[K_SPACE]:
            player.jump(jump_speed)

        #move the player with gravity
        player.move_y()

        #render the frame
        screen.blit(background, (bg_1_x, 0))
        screen.blit(background, (bg_2_x, 0))
        player_plain.draw(screen)
        world.update(screen)
        doom.update(screen)

        #update the display
        pygame.display.update()

        #check if the player is dead
        if doom.collided(player.rect):
            print("You Lose!")
            start = False
            finished = True

        #check if the player has completed the level
        if world.at_goal(player.rect):
            print("Winner!")
            start = False
            finished = True

        #set the speed
