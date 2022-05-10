class agent:
    def __init__(self, height, width, hp, dmg, W_Screen, H_Screen):
        self.height, self.width = height, width
        self.x = (W_Screen - self.width)/2
        self.y = (H_Screen- self.height)/2
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