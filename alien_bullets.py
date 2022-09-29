import pygame
from pygame.sprite import Sprite


#create Alien Bullets class
class Alien_Bullets(Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/red_laser.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.screen_height = 750

    def update(self):
        self.rect.y += 2
        if self.rect.top > self.screen_height:
            self.kill()