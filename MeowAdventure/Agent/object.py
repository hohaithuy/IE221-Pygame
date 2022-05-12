import pygame
class Object(pygame.sprite.Sprite):
        def __init__(self, x, y, path):
            super().__init__()

            self.x = x
            self.y = y
            self.image = pygame.image.load(path).convert_alpha()
            self.rect = self.image.get_rect(center = (self.x, self.y))
        