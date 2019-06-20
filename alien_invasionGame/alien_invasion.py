

import sys
import pygame
from pygame.sprite import Group  # import Group from pygame.sprite
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf


def run_game():

    # INITIALIZE GAME AND CREATE SCREEN OBJECT
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # MAKE A SHIP
    ship = Ship(ai_settings, screen)

    # MAKE A GROUP TO STORE BULLETS
    bullets = Group()  # make an instance of Group and call it bullets

    # MAKE AN ALIEN.
    aliens = Group()

    # CREATE THE FLEET OF ALIENS
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # START THE MAIN LOOP FOR THE GAME
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()


