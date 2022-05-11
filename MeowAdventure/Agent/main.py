from bat import Bat
from cat import Cat 
from smile import Smile
from frog import Frog
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

    # smile = Smile(10, 1)
    # smile.setLocation(player.getX() + 100, player.getY() + 50)
    # frog = Frog(10, 1)
    # frog.setLocation(player.getX() - 200, player.getY() - 10)
    # bat = Bat(10, 1)
    # bat.setLocation(player.getX() - 100, player.getY())
    
    run = True
    action = 'idle' #Hành động của nhân vật
    
    while run:
        #print(cat.getX(), cat.getY(), cat.getW(), cat.getH(), smile.getX(), smile.getY(), smile.getW(), smile.getH())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN: 
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    action = 'left'
                elif keys[pygame.K_RIGHT]:
                    action = 'right'
                elif keys[pygame.K_UP]:
                    action = 'jump'
                elif keys[pygame.K_DOWN]:
                    action = 'attack1'
                elif keys[pygame.K_SPACE]:
                    action = 'attack2'
                player.setAction()# reset lại thứ tự hành động mỗi khi thực hiện hoạt ảnh mới
            elif event.type == pygame.KEYUP: 
                action = 'idle'
                # player.setAction() 
                
        #drawing 
        windowns.fill((0, 0, 0))
        pygame.draw.line(windowns, 'blue', (0, 100), (900, 100))
        player.draw(windowns)
        # smile.drawAction(windowns, speedGame, player)
        # frog.drawAction(windowns, speedGame, player)
        # bat.drawAction(windowns, speedGame, player)
        player.update()        
        pygame.display.update()
        timer.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()