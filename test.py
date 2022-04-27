import pygame, sys
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Hello world!')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.fill((255, 255, 255))#Tô màu nền
    
    surface2rect = pygame.Surface((150, 50))
    surface2rect.fill((0, 255, 0))
    pygame.draw.rect(surface2rect, (255, 0, 0), (20, 20, 50, 20))
    DISPLAYSURF.blit(surface2rect, (100, 80))
    
    pygame.display.update()