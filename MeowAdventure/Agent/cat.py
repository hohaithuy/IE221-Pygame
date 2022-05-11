import pygame
import os
from agent import agent
	
      
class Cat(agent):
    
    def __init__(self, hp=10, dmg=1, W_Screen = 900, H_Screen = 500):
        agent.__init__(self, hp, dmg, W_Screen, H_Screen)

        self.suface = {'run' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "run/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "run")) ]
                        ,'idle' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "idle/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "idle")) ]
                        ,'jump' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "jump/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "jump")) ]
                        ,'attack1' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "attack1/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "attack1")) ]
                        ,'attack2' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "attack2/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "attack2")) ]
                        ,'takeDmg' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "takeDmg/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "takeDmg")) ]
                        ,'death' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "death/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "death")) ]
                        }
        
        self.action = 'idle'

        self.gravity = 0

        self.index = 0
        self.image = self.suface['idle'][int(self.index)]
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.framrate = 0.2
        self.isJump = False
        self.jumpCount = 15  
        self.vel = 0
        self.flip = False
    
    def setAction(self):
        #reset hành động mỗi lần bấm phím
        self.action = 0
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.action = 'jump'
            self.isJump = True

        if keys[pygame.K_RIGHT]:
            self.setX(self.x + (self.vel + 1))
            self.flip = False
        elif keys[pygame.K_LEFT]:
            self.setX(self.x - (self.vel + 1))
            self.flip = True

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -15:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1
                print(self.y)
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
            self.action = 'idle'
        if self.vel > 3: self.vel = 4
    
    def animations_state(self):
        self.index += self.framrate
        if self.index >= len(self.suface[self.action]):
            self.index = 0

        self.image = self.suface[self.action][int(self.index)]
        self.image = pygame.transform.flip(self.image, self.flip, False) 
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))

    def update(self):
        self.input()
        self.animations_state()
        self.jump()
        self.apply_velocity()

