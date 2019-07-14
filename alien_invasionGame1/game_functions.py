import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    # WATCH FOR KEYBOARD AND MOUSE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # else-if event for when a KEYDOWN is detected
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:  # moving right is set to False when we release the key
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key presses"""
    if event.key == pygame.K_RIGHT:  # check if the key pressed is the right arrow by reading event.key
        ship.moving_right = True  # ship.moving_right flag is true and begins to move continuously right.
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # REDRAW THE SCREEN DURING EACH PASS THROUGH THE LOOP.
    screen.fill(ai_settings.bg_color)
    # REDRAW ALL BULLETS BEHIND SHIP AND ALIENS
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # MAKE THE MOST RECENTLY DRAWN SCREEN VISIBLE
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    # UPDATE BULLET POSITION
    bullets.update()

    # GET RID OF BULLETS THAT HAVE DISAPPEARED.
    for bullet in bullets.copy():  # copy() method allows us to modify bullets inside the loop
        if bullet.rect.bottom <= 0:  # check to see if bullet has disappeared off top of screen
            bullets.remove(bullet)  # if yes then remove it from bullets

    # CHECK FOR ANY BULLETS THAT HAVE HIT ALIENS. IF SO GET RID OF BOTH.
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)  # create new bullet and add it to bullets group
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width  # using alien that was just created to get alien width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(ai_settings, screen)  # creates an alien
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # CREATE THE FLEET OF ALIENS
    for row_number in range(number_rows):  # set up loop that counts from 0 to the # of aliens
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat the same as if the ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if the fleet is at an edge, and then update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # LOOK FOR ALIEN-SHIP COLLISIONS.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # LOOK FOR ALIENS HITTING THE BOTTOM OF THE SCREEN.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

