import pygame
import os

class Portal(pygame.sprite.Sprite):
    
    def __init__(self, screen, player, x , y, action = 'start', framerate = 0.05, index = 0):
        super().__init__()
        self.x = x
        self.y = y 
        self.screen = screen
        self.player = player
        self.index = index
        self.action = action 
        self.framerate = framerate
        self.flip = True
        self.end = False
         
        self.suface = {'idle' : [pygame.transform.scale(pygame.image.load(os.path.join("res","portal", "idle", i)).convert_alpha(), (100, 100)) for i in os.listdir(os.path.join("res","portal", "idle")) ]
                    ,'start' : [pygame.transform.scale(pygame.image.load(os.path.join("res","portal", "start", i)).convert_alpha(), (100, 100)) for i in os.listdir(os.path.join("res","portal", "start")) ]
                    , 'end' : [pygame.transform.scale(pygame.image.load(os.path.join("res","portal", "end", i)).convert_alpha(), (100, 100)   ) for i in os.listdir(os.path.join("res","portal", "end")) ]
                    }
        self.image = self.suface['start'][int(self.index)]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))  
        
        
    def animations_state(self):
        self.index += self.framerate
        
        if int(self.index) >= len(self.suface[self.action]):
            if self.action == 'end':
                self.kill()
            
            self.action = 'idle'
            self.index = 0         

        self.image = self.suface[self.action][int(self.index)]
        self.image = pygame.transform.flip(self.image, self.flip, False) 
        self.image.set_colorkey((0, 0, 0))
        
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))  
        
    def checkCollide(self):
        sprite = self.player.sprites()[0]
        if abs(self.x - sprite.rect.x) <= 20 or abs(self.x - sprite.rect.left) <= 20:
            self.action = 'end'
            self.index = 0
            self.end = True
            sprite.Pause()
    
    def update(self):
        if self.end == False:
            self.checkCollide()
        self.animations_state()
        #print(self.action, int(self.index))
        
