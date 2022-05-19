from operator import index
from re import S
import pygame
import os

class Wall(pygame.sprite.Sprite):
    def __init__(self, screen, player, x , y, w, h, index = 4):
        super().__init__()
        self.x = x
        self.y = y - 100
        self.screen = screen
        self.player = player
        
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("background", "wall" + str(index) + ".png")).convert_alpha(), (w, h))
        self.image.set_colorkey((0, 0, 0))          
        self.rect = self.image.get_rect(topleft = (self.x, self.y))  
        
    def checkCollide(self):
        
        if self.player.sprites() != []:
            sprite = self.player.sprites()[0]
            if sprite.rect.bottom - self.rect.top <= 10 and sprite.rect.bottom - self.rect.top >= 0 and sprite.rect.center[0] >= self.rect.left and sprite.rect.center[0] <= self.rect.right:
                sprite.isJump = False
                sprite.setLocation(sprite.x, self.rect.top)
                sprite.jumpCount = 15

    def update(self):
        self.checkCollide()
        #print(self.action, int(self.index))
        # pygame.draw.rect(self.screen, 'blue', self.rect) 
        