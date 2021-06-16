import pygame
import pygame.camera

pygame.init()
pygame.camera.init()
from pygame.locals import *

size = (320, 240)

display = pygame.display.set_mode(size,0)

cam = pygame.camera.Camera("/dev/video0", size)
cam.start()

inverse = pygame.Surface(size, pygame.SRCALPHA)

for i in range (1,50):
    image = cam.get_image()
    lines = pygame.transform.laplacian(image)
    inverse.fill((255,255,255,255))
    inverse.blit(lines, (0,0), None, BLEND_RGB_SUB)
    display.blit(inverse, (0,0))
    pygame.display.flip()

pygame.image.save(inverse, "/home/pi/test.png")