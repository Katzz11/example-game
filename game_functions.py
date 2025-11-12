import sys
import pygame
from player import Player
from bubble import Bubble

pygame.init()
ADDBUBBLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBUBBLE, 250)


def check_events(game_settings, screen, player, bubbles, stats, play_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.moving_right = True
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            if event.key == pygame.K_UP:
                player.moving_up = True
            if event.key == pygame.K_DOWN:
                player.moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            if event.key == pygame.K_LEFT:
                player.moving_left = False
            if event.key == pygame.K_UP:
                player.moving_up = False
            if event.key == pygame.K_DOWN:
                player.moving_down = False
        elif event.type == ADDBUBBLE:
            create_bubble(game_settings, screen, bubbles)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y)


def check_play_button(stats, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True


def create_bubble(game_settings, screen, bubbles):
    new_bubble = Bubble(screen, game_settings)
    bubbles.add(new_bubble)


def kaboom(screen):
    """Flash the screen white and red briefly when player dies."""
    flash_colors = [(255, 255, 255), (255, 0, 0)]  # white & red
    for i in range(6):  # number of flashes
        screen.fill(flash_colors[i % 2])
        pygame.display.flip()
        pygame.time.delay(100)  # short delay per flash
    screen.fill((0, 0, 0))  # reset to black or bg
    pygame.display.flip()


def update_bubbles(player, bubbles, stats, sb):
    """Handle collisions and scoring."""
    hitted_bubble = pygame.sprite.spritecollideany(player, bubbles)
    if hitted_bubble is not None:
        # If it's a black bubble → KABOOM 💣
        if hitted_bubble.color == (0, 0, 0):
            kaboom(player.screen)
            stats.game_active = False
            bubbles.empty()
            print("kaboom, rico? yes rico. kaboom.")
        else:
            stats.score += hitted_bubble.bubble_radius
            sb.prepare_score()
            hitted_bubble.kill()


def update_screen(game_settings, screen, player, bubbles, clock, stats, play_button, sb):
    screen.fill(game_settings.bg_color)
    player.blit_me()
    if len(bubbles) > 0:
        for bubble in bubbles:
            bubble.blit_me()

    sb.draw_score()
    clock.tick(30)
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()