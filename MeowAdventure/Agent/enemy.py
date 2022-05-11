from enum import Flag
from operator import index
from optparse import check_choice
from turtle import width
import pygame
import os
from cat import Cat
from agent import agent

	

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, x, y, hp, dmg, W_Screen = 900, H_Screen = 500):
        
        super().__init__()

        self.x = x
        self.y = y
        self.hp = hp
        self.dmg = dmg
        self.isExist = False
        self.isRotate = False
        self.index = 0 #Hành động thứ mấy trong 
        self.attack = False
        self.flip = False
        
        self.W_Screen = W_Screen
        self.H_Screen = H_Screen
        self.framerate = 0.1#
        self.velocity = 2# >0: go right, <0: go left
        self.player = player
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getH(self):
        return self.height
    
    def getW(self):
        return self.width
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
        
    def getHP(self):
        return self.hp
    
    def setHP(self, hp):
        self.hp = hp
        
    # def setExist(self, exist):
    #     self.isExist = exist
        
    # def setRotate(self, rotate):
    #     self.isRotate = rotate
        
class Frog(Enemy):
    
    def __init__(self, screen, player,  hp = 5, dmg= 1, W_Screen = 900, H_Screen = 500, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, 200, 301, hp, dmg, W_Screen, H_Screen)
        self.screen = screen
        self.suface = {'run' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "run/", i)).convert_alpha()) for i in os.listdir(os.path.join("Frog", "run")) ]
                        ,'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "idle/", i)).convert_alpha()) for i in os.listdir(os.path.join("Frog", "idle")) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "attack/", i)).convert_alpha()) for i in os.listdir(os.path.join("Frog", "attack")) ]
                        ,'hit' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "hit/", i)).convert_alpha()) for i in os.listdir(os.path.join("Frog", "hit")) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "death/", i)).convert_alpha()) for i in os.listdir(os.path.join("Frog", "death")) ]
                        }
        self.action = action_name
        
        self.image = self.suface['idle'][int(self.index)]
        self.rect =  self.image.get_rect(midbottom = (self.x, self.y))
        self.flip_cat = False

    
    
    def islive(self):
        if self.getHP() <= 0:
            self.action = 'death'
        
    def update(self):
        self.animations_state()
        if self.checkCollide() == False:
            self.move()
        self.islive()
        #print(self.flip)
        
        
    def move(self):
        if self.rect.right >= self.W_Screen:
            self.velocity = -2
            
        elif self.rect.left <= 0:
            self.velocity = 2
        
        if self.velocity > 0:
            self.flip = False
        else: self.flip = True
        
        #print(self.action, self.rect.x)
        if self.action == 'run':
            self.setX(self.getX() + self.velocity)
            
    def animations_state(self):
        #if self.attack:
            #self.framerate = 2 / (20 - len(self.suface[self.action]))
            #print(self.framerate)


        self.index += self.framerate
        
        
        if self.index >= len(self.suface[self.action]):
            if self.attack:
                self.framerate = 0.1
                self.action = 'idle'
                self.attack = False
                
            elif self.action == 'idle':
                self.action = 'run'
            elif self.action == 'death':
                self.kill()
            self.index = 0

        self.image = self.suface[self.action][int(self.index)]
        self.image = pygame.transform.flip(self.image, self.flip, False) 
        
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))  
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        
        
        
    def attack(self):
        pass
        
    def checkCollide(self):
        hits = pygame.sprite.spritecollide(self, self.player , False)#get list spire in groups

        if hits != []:
            self.action = 'attack'
            self.framerate = 0.05
            self.attack = True
            self.flip = hits[0].rect.x < self.rect.x
            if int(self.index) >= 5: 
                hits[0].takeDmg(self.dmg)
                
            return True
        return False
    
    def takeDmg(self, dmg):
        self.setHP(self.getHP() - dmg)
        self.action = 'hit'
        
        
        
        
########################
########################
class Slime(Enemy):
    
    def __init__(self, screen, player,  hp = 5, dmg= 1, W_Screen = 900, H_Screen = 500, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, 100, 301, hp, dmg, W_Screen, H_Screen)
        self.screen = screen
        self.suface = {'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "idle/", i))) for i in os.listdir(os.path.join("Slime", "idle")) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "hop/", i))) for i in os.listdir(os.path.join("Slime", "hop")) ]
                        + [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "attack/", i))) for i in os.listdir(os.path.join("Slime", "attack")) ]
                        + [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "death/", i))) for i in os.listdir(os.path.join("Slime", "death")) ]
                        }
        self.action = action_name
        
        self.image = self.suface['idle'][int(self.index)]
        self.rect =  self.image.get_rect(midbottom = (self.x, self.y))

    
    
    def islive(self):
        if self.getHP() <= 0:
            self.action = 'death'
        
    def update(self):
        self.animations_state()
        self.checkCollide()
        self.islive()
        
        
        
    def animations_state(self):
        #if self.attack:
            #self.framerate = 2 / (20 - len(self.suface[self.action]))
            #print(self.framerate)


        self.index += self.framerate
        
        
        if self.index >= len(self.suface[self.action]):
            if self.attack:
                self.framerate = 0.1
                self.action = 'idle'
                self.attack = False

            elif self.action == 'death':
                self.kill()
            self.index = 0

        self.image = self.suface[self.action][int(self.index)]
        
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))  
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        
        
        
    def attack(self):
        pass
        
    def checkCollide(self):
        hits = pygame.sprite.spritecollide(self, self.player , False)#get list spire in groups

        if hits != []:
            self.action = 'attack'
            self.framerate = 0.1
            self.attack = True 
            hits[0].takeDmg(self.dmg)    
            return True
        return False
    
    def takeDmg(self, dmg):
        self.setHP(self.getHP() - dmg)
        self.action = 'hit'
