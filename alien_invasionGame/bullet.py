import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):  # Bullet class inherits from Sprite. Lets you group related elements in your game
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()  # inherits properly from Sprite
        self.screen = screen

        # CREATE A BULLET RECTANGLE AT (0,0) AND SET CORRECT POSITION
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,  # creating the bullets rectangle attribute
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx  # bullets center = same as ships center
        self.rect.top = ship.rect.top  # top of bullet = top of ship, appears to fire from top of ship

        # STORE THE BULLET'S POSITION AS A DECIMAL VALUE.
        self.y = float(self.rect.y)  # decimal value will allow us to make finer adjustment's

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # UPDATE THE DECIMAL POSITION OF THE BULLET.
        self.y -= self.speed_factor  # subtract the amount stored in self.speed_factor from self.y
        # UPDATE THE RECTANGLE POSITION
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
