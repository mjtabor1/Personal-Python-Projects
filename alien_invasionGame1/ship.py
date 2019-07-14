import pygame


class Ship():

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings  # turn the ai_settings parameter into an attribute to use it in update()

        # LOAD THE SHIP IMAGE AND GET ITS RECTANGLE.
        self.image = pygame.image.load('images/ship.bmp')  # returns a surface representing the ship
        self.rect = self.image.get_rect()  # get_rect() accesses the surface's rectangle attribute
        self.screen_rect = screen.get_rect()  # store the screen's rectangle in self.screen_rect

        # START EACH NEW SHIP AT THE BOTTOM CENTER OF THE SCREEN
        self.rect.centerx = self.screen_rect.centerx  # x-cord. of ships center set equal to the centerx attribute
        self.rect.bottom = self.screen_rect.bottom  # y-cord of ships bottom set equal to the screen's bottom attribute

        # STORE A DECIMAL VALUE FOR THE SHIP'S CENTER.
        self.center = float(self.rect.centerx)  # accurately store the ships position using float()

        # MOVEMENT FLAG. ADDING A MOVING RIGHT AND MOVING LEFT ATTRIBUTE IN THE __INIT__ METHOD
        self.moving_right = False  # initially set right movement to false
        self.moving_left = False  # initially set left movement to false

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:  # move's the ship right if the self.moving_right flag is true
            self.center += self.ai_settings.ship_speed_factor  # update self.center to move right
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor  # update self center fo move left

        # Update rectangle object from self.center
        self.rect.centerx = self.center  # controls the position of the ship

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)  # will draw the image to the screen at the position specified

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx