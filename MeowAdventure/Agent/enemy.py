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
        """
        """
        super().__init__()

        self.x = x
        self.y = y
        self.hp = hp
        self.dmg = dmg
        self.index = 0 #Hành động thứ mấy trong 
        
        self.isAttack = False # Đang tấn công
        self.istakeDmg = False # Đang bị tấn công
        self.delay = 0# Thơi gian bất tử khi bị tấn công
        self.attack = False
        self.isLife = True
        
        self.flip = False
        
        
        self.W_Screen = W_Screen
        self.H_Screen = H_Screen
        self.framerate = 0.1#
        self.velocity = 2# >0: go right, <0: go left
        self.player = player
        
        
    def resetAction(self):
        self.index = 0
        
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

        
class Frog(Enemy):
    
    def __init__(self, screen, player, x, y,  hp = 5, dmg= 1, W_Screen = 900, H_Screen = 500, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, x, y, hp, dmg, W_Screen, H_Screen)
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
        #self.flip_cat = False
                
    def move(self):
        if self.rect.right >= self.W_Screen:
            self.velocity = -2
            
        elif self.rect.left <= 0:
            self.velocity = 2
        
        if self.velocity > 0:
            self.flip = False
        else: self.flip = True

        if self.action == 'run':
            self.setX(self.getX() + self.velocity)
            
    def animations_state(self):
        self.index += self.framerate
        
           
        if int(self.index) >= len(self.suface[self.action]):
            if self.isAttack:
                self.framerate = 0.1
                self.action = 'idle'
                self.isAttack = False
                self.attack = True
                
            elif self.action == 'idle':
                self.action = 'run'
                
            elif self.action == 'death':
                self.kill()
                
            else: self.action = 'idle'
                
            self.index = 0
            
            if self.delay != 0:
                self.delay -= 1
            

        self.image = self.suface[self.action][int(self.index)]
        self.image = pygame.transform.flip(self.image, self.flip, False) 
        
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))  
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        
    def update(self):
        self.attackAction()
        self.animations_state()
        self.move()
        #print("HP", self.getHP(), self.action, int(self.index),len(self.suface[self.action]) -1)

        #print(self.action, "index", int(self.index))    
        
        
    def attackDmg(self, sprite):
        if self.delay == 0:
            self.framerate = 0.15
            self.action = 'attack'
            self.isAttack = True 
            self.delay = 3
            self.attack = True
            self.resetAction()
        
        if int(self.index) == 6 and self.attack and self.checkCollide():
            sprite.setVulnarable()
            sprite.takeDmg(self.dmg)
            self.attack = False
        
    def attackAction(self):
        sprite = self.player.sprites()[0]
        if abs(self.x - sprite.rect.right) <= 35 or abs(self.x - sprite.rect.left) <= 35:
            self.attackDmg(sprite)  
    
    def checkCollide(self):
        hits = pygame.sprite.spritecollide(self, self.player , False)#get list spire in groups

        if hits != []:
            return True
        return False
    
    def takeDmg(self, dmg):
        
        self.setHP(self.getHP() - dmg)
        if self.getHP() > 0:
            self.action = 'hit'
            self.resetAction()
            self.istakeDmg = True
        else:
            self.action = 'death'
            self.framerate = 0.05
            if self.isLife:
                self.resetAction()
                self.isLife = False
        
        
        
        
########################
########################
class Slime(Enemy):
    
    def __init__(self, screen, player, x, y, hp = 3, dmg= 1, W_Screen = 900, H_Screen = 500, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, x, y, hp, dmg, W_Screen, H_Screen)
        self.screen = screen
        self.suface = {'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "idle/", i))) for i in os.listdir(os.path.join("Slime", "idle")) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "hop/", i))) for i in os.listdir(os.path.join("Slime", "hop")) ]
                        + [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "attack/", i))) for i in os.listdir(os.path.join("Slime", "attack")) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "death/", i))) for i in os.listdir(os.path.join("Slime", "death")) ]
                        , 'hit' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "hit/", i))) for i in os.listdir(os.path.join("Slime", "hit")) ]
                        }

        
        self.action = action_name
        
        self.image = self.suface['idle'][int(self.index)]
        self.rect =  self.image.get_rect(midbottom = (self.x, self.y))
        self.music = pygame.mixer.Sound('Sound/slimejump.wav')
        
    def animations_state(self):
        self.index += self.framerate
        
        
        if round(self.index, 2) == 13.0 and self.isAttack:
            pygame.mixer.Sound.play(self.music)
            
        if int(self.index) >= len(self.suface[self.action]):
            
            if self.action == 'death':
                self.kill()
                
            elif self.isAttack:
                self.framerate = 0.1
                self.isAttack = False
                
            self.action = 'idle'
            self.resetAction()
            if self.delay != 0:
                self.delay -= 1

        self.image = self.suface[self.action][int(self.index)]
        
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))  
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        #pygame.draw.circle(self.screen, 'red', (self.x, self.y), 3)
        
    def attackDmg(self, sprite):
        if self.delay == 0:
            self.framerate = 0.2
            self.action = 'attack'
            self.isAttack = True 
            self.delay = 3
            self.attack = True
            self.resetAction()
        
        if int(self.index) == len(self.suface[self.action]) - 4 and self.attack and self.checkCollide():
            sprite.setVulnarable()
            sprite.takeDmg(self.dmg)
            self.attack = False
            
        
        
    def attackAction(self):
        sprite = self.player.sprites()[0]
        if abs(self.x - sprite.rect.right) <= 45 or abs(self.x - sprite.rect.left) <= 45:
            self.attackDmg(sprite)
            
            
    def checkCollide(self):
        hits = pygame.sprite.spritecollide(self, self.player , False)#get list spire in groups
        if hits != []:   
            return True
        return False
    
    def takeDmg(self, dmg):
        self.setHP(self.getHP() - dmg)
        if self.getHP() > 0:
            self.action = 'hit'
            self.resetAction()
            self.istakeDmg = True
        else:
            self.action = 'death'
            self.framerate = 0.05
            if self.isLife:
                self.resetAction()
                self.isLife = False

    def update(self):
        self.animations_state()
        self.attackAction()
        #print("HP", self.getHP(), self.action, self.index, int(self.index),len(self.suface[self.action]) -1)


######################
class Bat(Enemy):
    
    def __init__(self, screen, player,  hp = 3, dmg= 1, W_Screen = 900, H_Screen = 500, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, 200, 313 - 132, hp, dmg, W_Screen, H_Screen)
        self.screen = screen
        self.suface = {'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "idle/", i))) for i in os.listdir(os.path.join("Bat", "idle")) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "idlefly/", i))) for i in os.listdir(os.path.join("Bat", "idlefly")) ]
                        +[pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "fly/", i))) for i in os.listdir(os.path.join("Bat", "fly")) ]
                        + [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "attack/", i))) for i in os.listdir(os.path.join("Bat", "attack")) ]
                        ,'hit' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "hit/", i))) for i in os.listdir(os.path.join("Bat", "hit")) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "death/", i))) for i in os.listdir(os.path.join("Bat", "death")) ]
                        }

        
        self.action = action_name
        
        self.image = self.suface['idle'][int(self.index)]
        self.rect =  self.image.get_rect(midtop = (self.x, self.y))
        
    def animations_state(self):
        self.index += self.framerate
                  
        if int(self.index) >= len(self.suface[self.action]):
            if self.action == 'death':
                self.kill()
            elif self.isAttack:
                self.framerate = 0.1
                self.action = 'idle'
                self.isAttack = False

            self.resetAction()
            if self.delay != 0:
                self.delay -= 1

        self.image = self.suface[self.action][int(self.index)]
        
        self.rect = self.image.get_rect(midtop = (self.x, self.y))  
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        #pygame.draw.circle(self.screen, 'red', (self.x, self.y), 3)
        
    def attackDmg(self, sprite):
        if self.delay == 0:
            self.framerate = 0.2
            self.action = 'attack'
            self.isAttack = True 
            self.delay = 3
            self.attack = True
            self.resetAction()
           
        if int(self.index) == 17 and self.attack and self.checkCollide():
            sprite.setVulnarable()
            sprite.takeDmg(self.dmg)
            self.attack = False
        
        
    def attackAction(self):
        sprite = self.player.sprites()[0]
        if abs(self.x - sprite.rect.right) <= 25 or abs(self.x - sprite.rect.left) <= 25:
            self.attackDmg(sprite)     
            
    def checkCollide(self):
        hits = pygame.sprite.spritecollide(self, self.player , False)#get list spire in groups
        if hits != []:   
            return True
        return False
    
    def takeDmg(self, dmg):
        self.setHP(self.getHP() - dmg)
        if self.getHP() > 0:
            self.action = 'hit'
            self.resetAction()
            self.istakeDmg = True
        else:
            self.action = 'death'
            self.framerate = 0.05
            if self.isLife:
                self.resetAction()
                self.isLife = False

    def update(self):
        self.animations_state()
        self.attackAction()
        #print("HP", self.getHP(), self.action, int(self.index),len(self.suface[self.action]) -1)

