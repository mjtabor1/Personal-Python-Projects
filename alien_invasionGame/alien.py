import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # LOAD THE ALIEN IMAGE AND SET ITS RECTANGLE ATTRIBUTE.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # START EACH NEW ALIEN NEAR THE TOP LEFT OF THE SCREEN.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # STORE THE ALIEN'S EXACT POSITION.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)