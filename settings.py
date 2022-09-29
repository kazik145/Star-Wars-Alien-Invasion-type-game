import pygame
from pygame import mixer
class Settings:

    def __init__(self):
        """Initialize the game' static settings"""
        # Screen settings
        self.background = pygame.image.load('images/deathstar.jpg')
        self.colors = [(51, 255, 51), (51, 102, 255), (179, 0, 179)]
        self.screen_width = 1200
        self.screen_height = 650
        self.bg_color = (238, 219, 0)
        self.ship_limit = 3
        # audio settings
        self.mixer = mixer
        # Bullet settings
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 40
        self.bullet_color = (179, 0, 179)
        self.bullets_allowed = 3
        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        # scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def play_bg_music(self):
        """Playing background music"""
        self.mixer.music.load('music/Star Wars Theme.mp3')
        mixer.music.set_volume(0.5)
        self.mixer.music.play(-1)

    def play_blaster_sound(self):
        """Playing blaster sound"""
        self.mixer.Sound('music/blaster.mp3').play()

