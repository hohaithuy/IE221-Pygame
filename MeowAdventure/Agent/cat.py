import pygame
import os
from agent import agent
	
      
class Cat(agent, pygame.sprite.Sprite):
    
    def __init__(self, hp=10, dmg=1, W_Screen = 900, H_Screen = 500):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(200, 320, hp, dmg, W_Screen, H_Screen)

        self.suface = {'right' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "run/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "run")) ]
                        ,'idle' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "idle/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "idle")) ]
                        ,'jump' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "jump/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "jump")) ]
                        ,'attack1' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "attack1/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "attack1")) ]
                        ,'attack2' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "attack2/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "attack2")) ]
                        ,'takeDmg' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "takeDmg/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "takeDmg")) ]
                        ,'death' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "death/", i)).convert_alpha(), (100,100)) for i in os.listdir(os.path.join("MeowKnight", "death")) ]
                        }
        
        self.action = 'idle'

        self.gravity = 0
        self.suface['left'] = [pygame.transform.flip(i, True, False) for i in self.suface['right'] ]

        self.index = 0
        self.image = self.suface['idle'][int(self.index)]
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
    
    def setAction(self):
        #reset hành động mỗi lần bấm phím
        self.action = 0
    
    def input(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom >= 300:
            if keys[pygame.K_SPACE]:
                    self.gravity -= 20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.gravity = 0
            self.rect.bottom = 300

    def animations_state(self):
        self.index += 0.1
        if self.index >= len(self.suface[self.action]):
            self.index = 0
        self.image = self.suface[self.action][int(self.index)]


    def update(self):
        self.input()
        self.apply_gravity()
        self.animations_state()

    def drawAction(self, screen, action_name, speedGame):
        if action_name == 'right':
            self.setX(self.x + 1)
        elif action_name == 'left':
            self.setX(self.x - 1)
        elif action_name == 'jump':
            if self.action <= 5:
                self.setY(self.y - 2) # tăng từ hoạt ảnh 1 - 5, giảm sau 6 hành động sau- đang xử lý
            else:
                self.setY(self.y + 2)
        
        char = self.suface[action_name][int(self.action)]
        self.image = char.get_rect(midbottom = (self.x, self.y))
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))

        
        self.action += speedGame
        if self.action >= len(self.suface[action_name]):
            self.action = 0
    
#################    