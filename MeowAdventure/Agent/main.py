from cat import Cat 
from enemy import Frog, Slime, Bat
import pygame
from object import Object
import pygame
from states import States
import os

from pygame import mixer


WIDTH, HEIGHT = 900, 500
pygame.init()
mixer.init()
FPS = 60
timer = pygame.time.Clock()
speedGame = 0.1
state = 1
      
windowns = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MeowAdventure")

def main():

    player = pygame.sprite.GroupSingle()
    enemy = pygame.sprite.Group()
    portal = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    
    state = States(windowns, player, enemy, portal, wall)
    
    
    player.add(Cat(windowns, enemy))
    state.createState()
    
    run = True    
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        #drawing 
        
        #pygame.draw.line(windowns, 'blue', (0, 313), (900, 313))
        state.update()
             
        pygame.display.update()
        timer.tick(FPS)
    
    
    pygame.quit()

if __name__ == "__main__":
    main()
    
