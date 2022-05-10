import pygame
import os
from agent import agent
	
      
class Cat(agent):
    
    def __init__(self, hp, dmg, W_Screen = 900, H_Screen = 500):
        
        #path_cat = "./MeowAdventure/Agent/MeowKnight/"
        self.suface = {'right' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "run/", i)), (200,200)) for i in os.listdir(os.path.join("MeowKnight", "run")) ]
                        ,'idle' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "idle/", i)), (200,200)) for i in os.listdir(os.path.join("MeowKnight", "idle")) ]
                        ,'jump' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "jump/", i)), (200,200)) for i in os.listdir(os.path.join("MeowKnight", "jump")) ]
                        ,'attack1' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "attack1/", i)), (200,200)) for i in os.listdir(os.path.join("MeowKnight", "attack1")) ]
                        ,'attack2' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "attack2/", i)), (200,200)) for i in os.listdir(os.path.join("MeowKnight", "attack2")) ]
                        ,'takeDmg' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "takeDmg/", i)), (200,200)) for i in os.listdir(os.path.join("MeowKnight", "takeDmg")) ]
                        ,'death' : [pygame.transform.scale(pygame.image.load(os.path.join("MeowKnight", "death/", i)), (200,200)) for i in os.listdir(os.path.join("MeowKnight", "death")) ]
                        }
        
        
        
        self.suface['left'] = [pygame.transform.flip(i, True, False) for i in self.suface['right'] ]
        super().__init__(200, 200, hp, dmg, W_Screen, H_Screen)
        
    
    def setAction(self):
        #reset hành động mỗi lần bấm phím
        self.action = 0
    
        
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
        charRect = char.get_rect(topleft = (self.x, self.y))

        screen.blit(char, charRect)
        
        self.action += speedGame
        if self.action >= len(self.suface[action_name]):
            self.action = 0
    
#################    