import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from bullet import Bullet
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from button_1 import Button_1
from button_2 import Button_2
from button_3 import Button_3
from alien_bullets import Alien_Bullets
import random
from life import Life
from button_green import ButtonGreen
from button_blue import ButtonBlue
from button_purple import ButtonPurple
from choose_button import ButtonChoose
from coin import Coin


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.settings.play_bg_music()

        # Create an instance to store game statistics.
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()
        self.life_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()

        self.big_bullets_shots = []

        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.press_r_button = Button_1(self, "Press R to choose randomly")
        self.press_h_button = Button_2(self, "Press H to view All-time scoring list")
        self.press_esc_button = Button_3(self, "Press Esc to quit the game")
        self.press_g_button = ButtonGreen(self, "Press G")
        self.press_b_button = ButtonBlue(self, "Press B")
        self.press_prp_button = ButtonPurple(self, "Press P")
        self.choose_button = ButtonChoose(self, "Choose your side of the Power:")

        self.alien_cooldown = 1000
        self.life_cooldown = 60000
        self.coin_cooldown = 20000
        self.last_alien_shot = pygame.time.get_ticks()
        self.last_life = pygame.time.get_ticks()
        self.last_coin = pygame.time.get_ticks()
        self.bb_start = pygame.time.get_ticks()

    def _heal_ship(self):
        """Adding +1 to available ships"""
        if self.stats.ship_left < 4:
            self.stats.ship_left += 1
            self.sb.prep_ships()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullet_group.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # pause
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        # Make an alien.
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        alien_height = alien.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height)
        number_rows_y = available_space_y // (2 * alien_height)
        number_rows_y_even = []
        number_rows_y_odd = []
        for n in range(1, number_rows_y + 1):
            if n % 2 == 0:
                number_rows_y_even.append(n)
            else:
                number_rows_y_odd.append(n)

        # Create the first row of aliens.
        for row in range(len(number_rows_y_odd)):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                alien = Alien(self)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.y = 2 * alien_height + 2 * alien_height * row
                alien.rect.y = alien.y
                self.aliens.add(alien)
        for row in range(len(number_rows_y_even) + 1):
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                alien = Alien(self)
                alien.x = 50 + alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.y = alien_height + 2 * alien_height * row
                alien.rect.y = alien.y
                self.aliens.add(alien)

    def check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                # Look for alien-ship collisions.

                if pygame.sprite.spritecollideany(self.ship, self.aliens):
                    print('Ship hit!!!')
                    self._ship_hit()
                elif pygame.sprite.spritecollideany(self.ship, self.alien_bullet_group):
                    self._ship_hit()
                elif pygame.sprite.spritecollideany(self.ship, self.life_group):
                    self._heal_ship()
                    self.life_group.empty()

                self.ship.update()
                self._update_bullets()
                self.alien_bullet_group.update()
                self.life_group.update()
                self.coin_group.update()
                self.check_fleet_edge()
                self.aliens.update()

                # create random alien bullets
                # record current time
                time_now = pygame.time.get_ticks()
                # shoot
                if time_now - self.last_alien_shot > self.alien_cooldown and len(self.alien_bullet_group) < 5 and len(self.aliens) > 0:
                    attacking_alien = random.choice(self.aliens.sprites())
                    alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                    self.alien_bullet_group.add(alien_bullet)
                    self.last_alien_shot = time_now
                if time_now - self.last_life > self.life_cooldown and len(self.life_group) < 5:
                    one_life = Life(random.randint(10, 1100), 20)
                    self.life_group.add(one_life)
                    self.last_life = time_now
                if time_now - self.last_coin > self.coin_cooldown and len(self.coin_group) < 5:
                    one_coin = Coin(random.randint(10, 1100), 20)
                    self.coin_group.add(one_coin)
                    self.last_coin = time_now
            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Hide the mouse
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self.settings.bullet_color = (179, 0, 179)
            self.prepare_game()
        elif event.key == pygame.K_b and not self.stats.game_active:
            self.settings.bullet_color = (51, 102, 255)
            self.prepare_game()
        elif event.key == pygame.K_g and not self.stats.game_active:
            self.settings.bullet_color = (51, 255, 51)
            self.prepare_game()
        elif event.key == pygame.K_r and not self.stats.game_active:
            self.settings.bullet_color = random.choice(self.settings.colors)
            self.prepare_game()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.settings.play_blaster_sound()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if pygame.sprite.spritecollideany(self.ship, self.coin_group):
            self.stats.score += 1000
            self.coin_group.empty()
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1

            self.sb.prep_level()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def prepare_game(self):
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()
        # Reset the game statistics.
        self.stats.reset_stats()
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.settings.background, (0, 0))
        if self.stats.game_active:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.alien_bullet_group.draw(self.screen)
            self.life_group.draw(self.screen)
            self.coin_group.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.press_r_button.draw_button()
            self.press_esc_button.draw_button()
            self.press_g_button.draw_button()
            self.press_b_button.draw_button()
            self.press_prp_button.draw_button()
            self.choose_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()