import pygame
from pygame.sprite import Sprite


#create Alien Bullets class
class Life(Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/heart1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.screen_height = 750

    def update(self):
        self.rect.y += 1
        if self.rect.top > self.screen_height:
            self.kill()