from re import S
import pygame
import os
from enemy import Frog, Slime, Bat
from portal import Portal

class States():
    def __init__(self, screen, player, enemy, portal, lv = 3):
        self.lv = lv
        self.enemy = enemy
        self.player = player
        self.portal = portal
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load(os.path.join("background", "background-final" + str(self.lv) + ".png")), (self.screen.get_width(), self.screen.get_height()))
        self.isLvUp = False
    
    def loadImage(self):
        self.background = pygame.transform.scale(pygame.image.load(os.path.join("background", "background-final" + str(self.lv) + ".png")), (self.screen.get_width(), self.screen.get_height()))

    def createState(self):
        self.isLvUp = False

        if self.lv == 0:
            pass
        elif self.lv == 1:
            #self.enemy.add(Slime(self.screen, self.player, 500, 313))
            self.enemy.add(Slime(self.screen, self.player, 700, 313))
        elif self.lv == 2:
            self.loadImage()
            self.enemy.add(Frog(self.screen, self.player, 100, 313))
        
        elif self.lv == 3:
            self.loadImage()
            self.enemy.add(Frog(self.screen, self.player, 100, 313))

        
        if self.lv == 3:
            self.player.sprites()[0].setLocation(100, 442)
        elif self.lv != 1:
            self.player.sprites()[0].setLocation(100, 313)
            
    def update(self):
        #print(self.enemy.sprites)
        self.screen.fill((0, 0, 0))
        
        if self.isLvUp and self.portal.sprites() == []:
            self.lv += 1
            self.createState()
            
        if self.enemy.sprites() == [] and self.portal.sprites() == []:
            self.portal.add(Portal(self.screen, self.player, 800, 320))
            self.isLvUp = True

        self.screen.blit(self.background, (0, 0))
        
        self.enemy.draw(self.screen)
        self.portal.draw(self.screen)
        self.player.draw(self.screen)
        
        self.enemy.update()
        self.portal.update()
        self.player.update()
    
    def nextState(self):
        pass
