import pygame
import os
from agent import agent
	
      
class Cat(agent):
    
    def __init__(self, screen, enemy, x = 100, y = 313, hp=10
                 , dmg=1, W_Screen = 900, H_Screen = 500):
        agent.__init__(self, x, y, hp, dmg, W_Screen, H_Screen)
        self.suface = {'run' : [pygame.transform.scale2x(pygame.image.load(os.path.join("MeowKnight", "run/", i)).convert_alpha()) for i in os.listdir(os.path.join("MeowKnight", "run")) ]
                        ,'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("MeowKnight", "idle/", i)).convert_alpha()) for i in os.listdir(os.path.join("MeowKnight", "idle")) ]
                        ,'jump' : [pygame.transform.scale2x(pygame.image.load(os.path.join("MeowKnight", "jump/", i)).convert_alpha()) for i in os.listdir(os.path.join("MeowKnight", "jump")) ]
                        ,'attack1' : [pygame.transform.scale2x(pygame.image.load(os.path.join("MeowKnight", "attack1/", i)).convert_alpha()) for i in os.listdir(os.path.join("MeowKnight", "attack1")) ]
                        ,'attack2' : [pygame.transform.scale2x(pygame.image.load(os.path.join("MeowKnight", "attack2/", i)).convert_alpha()) for i in os.listdir(os.path.join("MeowKnight", "attack2")) ]
                        ,'takeDmg' : [pygame.transform.scale2x(pygame.image.load(os.path.join("MeowKnight", "takeDmg/", i)).convert_alpha()) for i in os.listdir(os.path.join("MeowKnight", "takeDmg")) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("MeowKnight", "death/", i)).convert_alpha()) for i in os.listdir(os.path.join("MeowKnight", "death")) ]
                        }
        
        self.action = 'idle'
        self.gravity = 0
        self.index = 0
        self.image = self.suface['idle'][int(self.index)]
        
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.framerate = 0.2
        self.isJump = False
        self.jumpCount = 15  
        self.vel = 0
        self.flip = False
        self.attack = False
        self.isVulnerable = True
        self.isAttack = False
        self.alive = True
        self.end = False
        self.enemy = enemy
        self.isPause = False
        
        self.music = pygame.mixer.Sound("Sound/sword-hit.wav")
        
    def resetAction(self):
        self.index = 0
    
    def Pause(self):
        self.isPause = True
    
    def Start(self):
        self.isPause = False
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.action = 'jump'
            self.isJump = True

        if keys[pygame.K_RIGHT]:
            x = self.x + (self.vel + 1)
            if x + 13 > self.W_screen:
                x = self.W_screen - 13
            self.setX(x)
            self.flip = False
            
        elif keys[pygame.K_LEFT]:
            x = self.x - (self.vel + 1)
            if x - 13 <= 0:
                x = 13
            self.setX(x)
            self.flip = True

        elif keys[pygame.K_a] and not self.isAttack:
            self.action = 'attack1'
            self.attack = True
            self.isAttack = True
            self.resetAction()

        elif keys[pygame.K_s] and not self.isAttack:
            self.action = 'attack2'
            self.isAttack = True
            self.attack = True
            self.resetAction()
            pygame.mixer.Sound.play(self.music)

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -15:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.action = 'idle'
                self.isJump = False
                self.jumpCount = 15
        
    def apply_velocity(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.vel += 0.1
            if self.action != 'jump':
                self.action = 'run'
        else:
            self.vel = 0
            if self.action == 'run': self.action = 'idle'
        if self.vel > 3: self.vel = 4
    
    def animations_state(self):
        if self.isAttack:
            self.framerate = 2 / (20 - len(self.suface[self.action]))
            
        self.index += self.framerate

        if self.index >= len(self.suface[self.action]):
            self.index = 0
            self.framerate = 0.2
            if self.isAttack:
                self.action = 'idle'
                self.isAttack = False
            if self.action == 'takeDmg':
                self.action = 'idle'
            
            if not self.alive:
                self.index = -1
                self.end = True
        
        if self.isJump == False and self.action == 'jump':
            self.action = "idle"
            self.resetAction()
        self.image = self.suface[self.action][int(self.index)]
        self.image = pygame.transform.flip(self.image, self.flip, False) 
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
    
    def takeDmg(self, dmg: int):
        if self.isVulnerable is True:
            self.isVulnerable = False
            self.setHP(self.getHP() -  dmg)
            self.action = 'takeDmg'
            self.framerate = 0.1
            self.index = 0
            #print("Take Dmg")

    def checkHP(self):
        if self.hp <= 0:
            self.alive = False
            self.action = 'death'
            self.framerate = 0.05
            self.index = 0
            pygame.mixer.Sound.play(self.music)
    

    def setVulnarable(self):
        self.isVulnerable = True

    def attackDmg(self, sprite):
        if self.action == "attack1" and self.attack and int(self.index) == 4:           
            sprite.takeDmg(self.dmg)
            self.attack = False
            
        elif self.action == "attack2" and self.attack and int(self.index) == 1:
            sprite.takeDmg(self.dmg)
            self.attack = False
            
            
    def checkCollide(self):
        hits = pygame.sprite.spritecollide(self, self.enemy , False)#get list spire in groups

        for sprite in hits:
            if self.isAttack:
                
                self.attackDmg(sprite)
                #sprite.takeDmg(self.dmg) 
       
    
    def update(self):
        if self.isPause == False:
            if self.alive:
                self.input()
                self.jump()
                self.apply_velocity()
                self.checkHP()
                self.checkCollide()
                #print("HP", self.getHP(), int(self.index), self.action)
            if not self.end:
                self.animations_state()

