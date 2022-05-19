import pygame
import os
from src.enemy import Frog, Slime, Bat, Golem
from src.wall import Wall
from src.portal import Portal

class States():
    """
    Lớp lưu trữ, quản lý trạng thái, các level của game
    """
    def __init__(self, screen, player, enemy, portal, wall, lv = 0):
        self.lv = lv
        self.enemy = enemy
        self.player = player
        self.portal = portal
        self.wall = wall 
        
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load(os.path.join("res","background", "background-final" + str(self.lv) + ".png")), (self.screen.get_width(), self.screen.get_height()))
        self.heart = [pygame.transform.scale(pygame.image.load(os.path.join("res","background", "heart" + str(i +1) + ".png")).convert_alpha(), (25, 25)) for i in range(3) ]
        self.music = pygame.mixer.Sound("res/Sound/backgroundmusic-scene12.wav")
        #self.heart.set_colorkey((0, 0, 0))
        self.isLvUp = False
    
    def loadImage(self, index):
        return pygame.image.load(os.path.join("res","background", "background-final" + str(index) + ".png"))

    
    
    def menuStart(self):
        self.player.sprites()[0].Pause()
        
        # while(True):
        #     keys = pygame.key.get_pressed()
            
                
        #     if keys[pygame.K_UP]:
        #         pass

        #     elif keys[pygame.K_DOWN] and not self.isAttack:
        #         pass
            
        #     elif keys[pygame.K_KP_ENTER]:
        #         self.lv += 1
        #         self.player.sprites()[0].Start()
        #         break

    def createState(self):
        self.isLvUp = False
        self.player.sprites()[0].Start()
        
        self.background = pygame.transform.scale(self.loadImage(self.lv), (self.screen.get_width(), self.screen.get_height()))
        self.wall.empty()

        if self.lv != 1:
            self.player.sprites()[0].setLocation(100, 100)
            
        if self.lv == 0:
            
            self.wall.add(Wall(self.screen, self.player, 0, 409, 1151/1.278, 277/1.43, 1))
            self.menuStart()
        elif self.lv == 1:
            pygame.mixer.Sound.play(self.music, -1)
            #self.enemy.add(Slime(self.screen, self.player, 500, 313))
            self.enemy.add(Frog(self.screen, self.player, 700, 313))
            self.wall.add(Wall(self.screen, self.player, 0, 409, 1151/1.278, 277/1.43, 1))
            
        elif self.lv == 2:
            pygame.mixer.Sound.stop(self.music)
            pygame.mixer.Sound.play(self.music, -1)
            self.enemy.add(Frog(self.screen, self.player, 700, 437))
            self.enemy.add(Bat(self.screen, self.player, 400, 355))
            self.enemy.add(Slime(self.screen, self.player, 370, 134))
            
            self.wall.add(Wall(self.screen, self.player, 384/1.92, 234, 494/1.92, 24/2.16, 2))
            self.wall.add(Wall(self.screen, self.player, 0, 412, 289/1.92, 411/2.16, 3))
            self.wall.add(Wall(self.screen, self.player, 370, 460, 192/1.92, 24/2.16, 4))
            
            self.wall.add(Wall(self.screen, self.player, 290/1.92, 412, 192/1.92, 24/2.16, 4))
            self.wall.add(Wall(self.screen, self.player, 287/1.92, 545, 389/1.92, 121/2.16, 5))
            self.wall.add(Wall(self.screen, self.player, 676/1.92, 575, 288/1.92, 56/2.16, 6))
            self.wall.add(Wall(self.screen, self.player, 966/1.92, 535, 765/1.92, 144/2.16, 7))
            self.wall.add(Wall(self.screen, self.player, 320/1.92, 320, 212/1.92, 75/2.16, 8))
           
        
        elif self.lv == 3:
            pygame.mixer.Sound.stop(self.music)
            self.music = pygame.mixer.Sound("res/Sound/backgroundmusic-scene3.wav")
            pygame.mixer.Sound.play(self.music, -1)
            self.player.sprites()[0].setLocation(100, 442)
            self.enemy.add(Golem(self.screen, self.player, 800, 300))
            self.wall.add(Wall(self.screen, self.player, 88/1.28, 435, 212/1.28, 75/1.448, 8))
            self.wall.add(Wall(self.screen, self.player, 413/1.28, 340, 228/1.28, 120/1.448, 9))
            self.wall.add(Wall(self.screen, self.player, 759/1.28, 410, 320/1.28, 73/1.448, 10))
            self.wall.add(Wall(self.screen, self.player, 0, 535, 1152/1.28, 85/1.448, 11))
            

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        
        for i in range(5):
            if i <=  self.player.sprites()[0].getHP() //2 -1:
                self.screen.blit(self.heart[0], (30 *i + 5, 10))
            elif i == self.player.sprites()[0].getHP() //2:
                if self.player.sprites()[0].getHP() %2 == 1:
                    self.screen.blit(self.heart[1], (30 *i + 5, 10))
                else:
                    self.screen.blit(self.heart[2], (30 *i + 5, 10))
            else:
                self.screen.blit(self.heart[2], (30 *i + 5, 10))
                
        self.wall.draw(self.screen)
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        self.portal.draw(self.screen)
        
        
        
        
    def update(self):
        if self.isLvUp and self.portal.sprites() == []:
            self.lv += 1
            self.createState()
            
        if self.enemy.sprites() == [] and self.portal.sprites() == [] and self.lv != 0:
            
            if self.lv == 2:
                self.portal.add(Portal(self.screen, self.player, 850, 460))
            else:
                self.portal.add(Portal(self.screen, self.player, 800, 320))
            self.isLvUp = True

        self.draw()
        self.wall.update()
        self.player.update()
        self.enemy.update()
        self.portal.update()
       

