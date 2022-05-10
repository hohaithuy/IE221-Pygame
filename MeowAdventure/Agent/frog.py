import pygame
import os
from agent import agent

	
def rectCollision(rect1, rect2):
    """Kiểm tra va chạm

    Args:
        rect1 (_list_): x, y, w, h 
        rect2 (_list_): x, y, w, h
    """
    #if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
    if rect1[0] == rect2[0]:
        return True
    return False 
 
class Frog(agent):
    
    def __init__(self, hp, dmg, W_Screen = 900, H_Screen = 500, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        
        self.suface = {'right' : [pygame.transform.scale(pygame.image.load(os.path.join("Frog", "run/", i)), (300, 300)) for i in os.listdir(os.path.join("Frog", "run")) ]
                        ,'idle' : [pygame.transform.scale(pygame.image.load(os.path.join("Frog", "idle/", i)), (300, 300)) for i in os.listdir(os.path.join("Frog", "idle")) ]
                        ,'attack' : [pygame.transform.scale(pygame.image.load(os.path.join("Frog", "attack/", i)), (300, 300)) for i in os.listdir(os.path.join("Frog", "attack")) ]
                        ,'hit' : [pygame.transform.scale(pygame.image.load(os.path.join("Frog", "hit/", i)), (300, 300)) for i in os.listdir(os.path.join("Frog", "hit")) ]
                        ,'death' : [pygame.transform.scale(pygame.image.load(os.path.join("Frog", "death/", i)), (300, 300)) for i in os.listdir(os.path.join("Frog", "death")) ]
                        }
        self.suface['left'] = [pygame.transform.flip(i, True, False) for i in self.suface['right'] ]
        self.action_name = action_name
        super().__init__(300, 300, hp, dmg, W_Screen, H_Screen)
        
    
    def setAction(self):
        #reset hành động mỗi lần bấm phím
        self.action = 0
    
    def attack(self):
        self.action_name = "attack"
        
    def drawAction(self, screen, speedGame, cat):
        
        char = self.suface[self.action_name][int(self.action)]
        charRect = char.get_rect(topleft = (self.x, self.y))
        self.action += speedGame

        if rectCollision([self.getX(), self.getY(), self.getW(), self.getH()], [cat.getX(), cat.getY(), cat.getW(), cat.getH()]):
            self.attack()
            self.action += 0.1
        
        
        if self.isExist:
            screen.blit(char, charRect)
        
        if self.action >= len(self.suface[self.action_name]):
            if self.action_name == "attack":
                self.setExist(False)
            self.action = 0
    
    def setLocation(self, x, y):
        self.setX(x)
        self.setY(y)
    
    
     