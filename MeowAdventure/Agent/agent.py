from threading import Timer
import pygame
import os
import time

class agent:
    def __init__(self, height, width, hp, dmg):
        self.height, self.width = height, width
        self.x = (WIDTH - self.width)/2
        self.y = (HEIGHT- self.height)/2
        self.hp = hp
        self.dmg = dmg
        self.isExist = 0
        self.isRotate = 0
        self.action = 0 #Hành động thứ mấy trong 
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
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
	
      
class Cat(agent):
    
    def __init__(self, hp, dmg):
        
        path_cat = "./MeowAdventure/Agent/MeowKnight/"
        self.suface = {'right' : [pygame.transform.scale(pygame.image.load(path_cat + "run/" + i), (200,200)) for i in os.listdir(path_cat + "run") ]
                        ,'idle' : [pygame.transform.scale(pygame.image.load(path_cat + "idle/" + i), (200,200)) for i in os.listdir(path_cat + "idle") ]
                        ,'jump' : [pygame.transform.scale(pygame.image.load(path_cat + "jump/" + i), (200,200)) for i in os.listdir(path_cat + "jump") ]
                        ,'attack1' : [pygame.transform.scale(pygame.image.load(path_cat + "attack1/" + i), (200,200)) for i in os.listdir(path_cat + "attack1") ]
                        ,'attack2' : [pygame.transform.scale(pygame.image.load(path_cat + "attack2/" + i), (200,200)) for i in os.listdir(path_cat + "attack2") ]
                        ,'takeDmg' : [pygame.transform.scale(pygame.image.load(path_cat + "takeDmg/" + i), (200,200)) for i in os.listdir(path_cat + "takeDmg") ]
                        ,'death' : [pygame.transform.scale(pygame.image.load(path_cat + "death/" + i), (200,200)) for i in os.listdir(path_cat + "death") ]
                        }
        self.suface['left'] = [pygame.transform.flip(i, True, False) for i in self.suface['right'] ]
        super().__init__(200, 200, hp, dmg)
        
    
    def setAction(self):
        #reset hành động mỗi lần bấm phím
        self.action = 0
    
        
    def drawAction(self, screen, action):
        if action == 'right':
            self.setX(self.x + 1)
        elif action == 'left':
            self.setX(self.x - 1)
        elif action == 'jump':
            if self.action <= 5:
                self.setY(self.y - 2) # tăng từ hoạt ảnh 1 - 5, giảm sau 6 hành động sau- đang xử lý
            else:
                self.setY(self.y + 2)
            
        screen.blit(self.suface[action][int(self.action)], (self.x, self.y))
        
        self.action += speedGame
        if self.action >= len(self.suface[action]):
            self.action = 0
            

WIDTH, HEIGHT = 900, 500
pygame.init()
FPS = 60
timer = pygame.time.Clock()
speedGame = 0.2
      
windowns = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MeowAdventure")


def main():
    cat = Cat(10, 1)
    run = True
    action = 'idle' #Hành động của nhân vật
    
    while run:
        print(action)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN: 
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    action = 'left'
                elif keys[pygame.K_RIGHT]:
                    action = 'right'
                elif keys[pygame.K_UP]:
                    action = 'jump'
                elif keys[pygame.K_DOWN]:
                    action = 'attack1'
                elif keys[pygame.K_SPACE]:
                    action = 'attack2'
                cat.setAction()# reset lại thứ tự hành động mỗi khi thực hiện hoạt ảnh mới
            elif event.type == pygame.KEYUP: 
                action = 'idle'
                cat.setAction()  
                
        #drawing 
        windowns.fill((0, 0, 0))
        pygame.draw.line(windowns, 'blue', (0, 320), (900, 320))
        cat.drawAction(windowns, action)
        pygame.display.update()
        timer.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()