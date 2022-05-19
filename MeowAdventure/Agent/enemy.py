import imp
import pygame
import os
from Mysort import MySort

	

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
    
    def __init__(self, screen, player, x, y,  hp = 7, dmg= 1, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, x, y, hp, dmg)
        self.screen = screen
        self.suface = {'run' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "run/", i)).convert_alpha()) for i in MySort(os.listdir(os.path.join("Frog", "run"))) ]
                        ,'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "idle/", i)).convert_alpha()) for i in MySort(os.listdir(os.path.join("Frog", "idle"))) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "attack/", i)).convert_alpha()) for i in MySort(os.listdir(os.path.join("Frog", "attack"))) ]
                        ,'hit' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "hit/", i)).convert_alpha()) for i in MySort(os.listdir(os.path.join("Frog", "hit"))) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Frog", "death/", i)).convert_alpha()) for i in MySort(os.listdir(os.path.join("Frog", "death"))) ]
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
            if self.action == 'death':
                self.kill()
            elif self.isAttack:
                self.framerate = 0.1
                self.action = 'idle'
                self.isAttack = False
                self.attack = True
                
            elif self.action == 'idle':
                self.action = 'run'
                
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
        
        if (int(self.index) == 6 or int(self.index) == 10) and self.attack and self.checkCollide():
            sprite.setVulnarable()
            sprite.takeDmg(self.dmg)
            self.attack = False
        
    def attackAction(self):
        sprite = self.player.sprites()[0]
        if (abs(self.x - sprite.rect.right) <= 35 or abs(self.x - sprite.rect.left) <= 35) and self.rect.center[1] <= sprite.rect.bottom and self.rect.center[1] >= sprite.rect.top:
            
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
    
    def __init__(self, screen, player, x, y, hp = 7, dmg = 1, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, x, y, hp, dmg)
        self.screen = screen
        self.suface = {'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "idle/", i))) for i in MySort(os.listdir(os.path.join("Slime", "idle"))) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "hop/", i))) for i in MySort(os.listdir(os.path.join("Slime", "hop"))) ]
                        + [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "attack/", i))) for i in MySort(os.listdir(os.path.join("Slime", "attack"))) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "death/", i))) for i in MySort(os.listdir(os.path.join("Slime", "death"))) ]
                        , 'hit' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Slime", "hit/", i))) for i in MySort(os.listdir(os.path.join("Slime", "hit"))) ]
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
        if (abs(self.x - sprite.rect.right) <= 45 or abs(self.x - sprite.rect.left) <= 45) and self.rect.center[1] <= sprite.rect.bottom and self.rect.center[1] >= sprite.rect.top:
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
    
    def __init__(self, screen, player, x, y, hp = 1, dmg= 1, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, x, y - 132, hp, dmg)
        self.screen = screen
        self.suface = {'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "idle/", i))) for i in MySort(os.listdir(os.path.join("Bat", "idle"))) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "idlefly/", i))) for i in MySort(os.listdir(os.path.join("Bat", "idlefly"))) ]
                        +[pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "fly/", i))) for i in MySort(os.listdir(os.path.join("Bat", "fly"))) ]
                        + [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "attack/", i))) for i in MySort(os.listdir(os.path.join("Bat", "attack"))) ]
                        ,'hit' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "hit/", i))) for i in MySort(os.listdir(os.path.join("Bat", "hit"))) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Bat", "death/", i))) for i in MySort(os.listdir(os.path.join("Bat", "death"))) ]
                        }

        
        self.action = action_name
        
        self.image = self.suface['idle'][int(self.index)]
        self.rect =  self.image.get_rect(midtop = (self.x, self.y))
        
    def animations_state(self):
        self.index += self.framerate
        
        
        if self.isAttack and int(self.index) >= 17 and self.attack and self.checkCollide():
            sprite = self.player.sprites()[0]
            sprite.setVulnarable()
            sprite.takeDmg(self.dmg)
            self.attack = False
            
        if int(self.index) >= len(self.suface[self.action]):
            if self.action == 'death':
                self.kill()
            elif self.isAttack:
                self.framerate = 0.1
                self.action = 'death'
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
            self.delay = 4
            self.attack = True
            self.resetAction()
        #print(int(self.index))
        
        
        
    def attackAction(self):
        sprite = self.player.sprites()[0]
        rect = (self.suface['attack'][17]).get_rect(midtop = (self.x, self.y))
        
        if (abs(self.x - sprite.rect.right) <= 25 or abs(self.x - sprite.rect.left) <= 25) and rect.bottom >= sprite.rect.bottom and rect.top <= sprite.rect.top:
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
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        
########################
class Golem(Enemy):
    
    def __init__(self, screen, player, x, y, hp = 40, dmg= 1, action_name = "idle"):  
        """_summary_

        Args:
            attack = hop + attack + death.
        """
        super().__init__(player, x, y, hp, dmg)
        self.screen = screen
        self.suface = {'idle' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Golem", "idle/", i))) for i in MySort(os.listdir(os.path.join("Golem", "idle"))) ]
                        + [pygame.transform.scale2x(pygame.image.load(os.path.join("Golem", "glow/", i))) for i in MySort(os.listdir(os.path.join("Golem", "glow"))) ]
                        ,'attack' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Golem", "attack/", i))) for i in MySort(os.listdir(os.path.join("Golem", "attack"))) ]
                        ,'laser' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Golem", "laser/", i))) for i in MySort(os.listdir(os.path.join("Golem", "laser"))) ]
                        ,'death' : [pygame.transform.scale2x(pygame.image.load(os.path.join("Golem", "death/", i))) for i in MySort(os.listdir(os.path.join("Golem", "death"))) ]
                        }

        self.weapon = pygame.sprite.Group()
        self.action = action_name
        self.flip = True
        self.image = self.suface['idle'][int(self.index)]
        self.rect =  self.image.get_rect(midtop = (self.x, self.y))
        self.power = 0
        
    def animations_state(self):
        self.index += self.framerate
        if self.action == 'laser':
            self.power = 0
        if int(self.index) >= len(self.suface[self.action]):
            if self.action == 'death':
                self.kill()
            elif self.isAttack:
                self.framerate = 0.2
                self.action = 'idle'
                self.isAttack = False

            self.resetAction()
            if self.delay != 0:
                self.delay -= 1

        self.image = self.suface[self.action][int(self.index)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.3, self.image.get_height() *1.3))
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_rect(midtop = (self.x, self.y))  
        
    def attackDmg(self, sprite):
        if self.delay == 0:
                     
            self.isAttack = True 
            self.delay = 3
            self.attack = True
            self.resetAction()
            
            if self.power == 3:
                self.action = 'laser'
                self.framerate = 0.05
                self.weapon.add(Weapon(self.screen, self.player,self.rect.midtop[0], sprite.rect.top, 'laser')) 
            else:
                self.action = 'attack'
                self.power += 1
 
        
        if self.weapon.sprites() != []:
            if int(self.index) >= 4 and self.action == 'laser' and self.weapon.sprites()[0].checkCollide() and self.attack :
                sprite.setVulnarable()
                sprite.takeDmg(self.dmg)
                self.attack = False
        elif int(self.index) >= 6 and self.action == 'attack' and self.checkCollide() and self.attack:
            sprite.setVulnarable()
            sprite.takeDmg(self.dmg)
            self.attack = False
            
        
    def attackAction(self):
        """_summary_
        """
        sprite = self.player.sprites()[0]
        if self.power == 3 and abs(self.x - sprite.rect.right) <= 900:
            self.attackDmg(sprite)    
        elif abs(self.x - sprite.rect.right) <= 70:
            self.attackDmg(sprite)
            
    
    def takeDmg(self, dmg):
        self.setHP(self.getHP() - dmg)
        if self.getHP() > 0:
            self.action = 'idle'
            self.resetAction()
            self.istakeDmg = True
        else:
            self.action = 'death'
            self.framerate = 0.05
            if self.isLife:
                self.resetAction()
                self.isLife = False

    
    def checkCollide(self):
            hits = pygame.sprite.spritecollide(self, self.player , False)#get list spire in groups
            if hits != []:   
                return True
            return False
    
    def update(self):
        
        self.animations_state()
        self.attackAction()
        
        if self.weapon.sprites() != []:
            self.weapon.draw(self.screen)
            self.weapon.update()
       
        
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        
        #print("HP", self.getHP(), self.action, int(self.index),len(self.suface[self.action]) -1)



class Weapon(pygame.sprite.Sprite):
    def __init__(self, screen, player, x , y, action = 'shoot'):
        super().__init__()
        self.x = x
        self.y = y
        self.screen = screen
        self.player = player
        self.action = action
        self.index = 0
        self.flip = True
        self.framerate = 0.1
        self.suface = {'shoot' : [pygame.transform.scale(pygame.image.load(os.path.join("Golem", "shoot/", i)).convert_alpha(), (200, 200)) for i in MySort(os.listdir(os.path.join("Golem", "shoot"))) ]
                        ,'laser' : [pygame.transform.scale(pygame.image.load(os.path.join("Golem", "laser_weapon/", i)).convert_alpha(), (900, 100)) for i in (MySort(os.listdir(os.path.join("Golem", "laser_weapon")))) ]
        }
        self.image = self.suface[self.action][0]
        self.image = pygame.transform.flip(self.image, self.flip, False) 
        #self.image.set_colorkey((0, 0, 0))    
        #a = (sorted(MySort(os.listdir(os.path.join("Golem", "laser_weapon")))) 
        #print(a)     
        self.rect = self.image.get_rect(midright = (self.x, self.y))  
        #print(self.x, self.rect.right)
        
    def animations_state(self):            
        self.index += self.framerate

        if int(self.index) >= len(self.suface[self.action]):
            self.index = 0
            #self.framerate = 0.2
            self.kill()

        self.image = self.suface[self.action][int(self.index)]
        self.image = pygame.transform.flip(self.image, self.flip, False) 
        self.rect = self.image.get_rect(midright = (self.x, self.y))
        
    def checkCollide(self):
            hits = pygame.sprite.spritecollide(self, self.player , False)#get list spire in groups
            if hits != []:   
                return True
            return False
                
    def update(self):
        self.animations_state()
        #pygame.draw.rect(self.screen, 'blue', self.rect) 
        print(self.action, int(self.index))
        #print(self.action, int(self.index)) 