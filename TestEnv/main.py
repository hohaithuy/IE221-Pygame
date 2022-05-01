import pygame
import os

# Global variable
WIDTH, HEIGHT = 900, 500
COLOR = (119, 140, 224)

FPS = 60
SCALE = (55, 40)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, SCALE), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, SCALE), -90)

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hello world!')




def draw_window():
        DISPLAYSURF.fill(COLOR)#Tô màu nền
        

        DISPLAYSURF.blit(YELLOW_SPACESHIP, (300, 200))
        DISPLAYSURF.blit(RED_SPACESHIP, (500, 200))
        pygame.display.update()

def main():

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()
if __name__ == "__main__":
    main()