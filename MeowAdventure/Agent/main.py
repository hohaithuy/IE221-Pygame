from bat import Bat
from cat import Cat 
from smile import Smile
from enemy import Frog, Slime
from threading import Timer
import pygame
import os
import time


WIDTH, HEIGHT = 900, 500
pygame.init()
FPS = 60
timer = pygame.time.Clock()
speedGame = 0.1
      
windowns = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MeowAdventure")


    


def main():
    player = pygame.sprite.GroupSingle()
    player.add(Cat())
    
    enemy = pygame.sprite.Group()
    enemy.add(Frog(windowns, player))
    enemy.add(Slime(windowns, player))

    run = True    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        #drawing 
        windowns.fill((0, 0, 0))
        pygame.draw.line(windowns, 'blue', (0, 300), (900, 300))
        player.draw(windowns)
        enemy.draw(windowns)
        
        # smile.drawAction(windowns, speedGame, player)
        # frog.drawAction(windowns, speedGame, player)
        # bat.drawAction(windowns, speedGame, player)
        enemy.update()
        player.update()
        enemy.update()        
        pygame.display.update()
        timer.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()