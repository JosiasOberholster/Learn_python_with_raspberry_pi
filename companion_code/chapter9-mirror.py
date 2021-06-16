import pygame
import pygame.camera

pygame.init()
pygame.camera.init()

display = pygame.display.set_mode((640,480),0)

cam = pygame.camera.Camera("/dev/video0", (640,480))
cam.start()

while True:
    image = cam.get_image()
    display.blit(image, (0,0))
    pygame.display.flip()