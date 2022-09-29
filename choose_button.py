import pygame.font


class ButtonChoose:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Set the dimensions and properties of the button.
        self.width, self.height = 360, 50
        self.button_color = (0, 0, 0)
        self.text_color = (238, 219, 0)
        self.font = pygame.font.SysFont(None, 58)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(810, 540, self.width, self.height)
        self.rect.centery = 250
        self.rect.centerx = self.screen_rect.centerx

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)