import pygame
class agent(pygame.sprite.Sprite):
    def __init__(self, hp, dmg, W_Screen, H_Screen):
        
        super().__init__()

        self.x = 300
        self.y = 300
        self.hp = hp
        self.dmg = dmg
        self.isExist = True
        self.isRotate = True
        self.action = 0 #Hành động thứ mấy trong 
        
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
        
    def setExist(self, exist):
        self.isExist = exist
        
    def setRotate(self, rotate):
        self.isRotate = rotate