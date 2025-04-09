import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE

def main():
    pygame.init()
    screen_width, screen_height = 900, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flash Capture Game")
    clock = pygame.time.Clock()

    # Load and scale background
    background = pygame.image.load("assets/background.PNG")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # Load alien images (29 total in fixed order)
    aliens = []
    for i in range(1, 30):
        alien = pygame.image.load(f"assets/alien{i}.png").convert_alpha()
        alien = pygame.transform.smoothscale(alien, (100, 100))
        aliens.append(alien)

    # Flash durations per level (ms)
    flash_times = [
        500, 475, 450, 425, 400, 375, 350, 325, 300, 275,
        250, 230, 210, 200, 200, 200, 200, 200, 200, 200, 190
    ]

    # Points awarded per level
    level_points = [
        1, 1, 1, 1, 1,
        5, 5, 5, 5, 5,
        10, 10, 10, 10,
        20, 20, 20, 20,
        25, 25,
        50
    ]

    # Fixed alien sequences per level
    levels = []
    idx = 0
    for _ in range(14):  # Levels 1–14: 1 alien
        levels.append([aliens[idx]])
        idx += 1
    for _ in range(4):   # Levels 15–18: 2 aliens
        levels.append([aliens[idx], aliens[idx+1]])
        idx += 2
    for _ in range(2):   # Levels 19–20: 3 aliens
        levels.append([aliens[idx], aliens[idx+1], aliens[idx+2]])
        idx += 3
    levels.append([aliens[idx]])  # Level 21

    # Fonts
    font_small = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 60)

    # Game state
    level = 0
    lives = 3
    score = 0
    state = "playing"
    message_timer = 0
    current_alien_index = 0
    alien_visible = False
    alien_rect = None
    alien_timer_start = 0
    alien_delay_timer = 0
    current_alien = None

    def draw_text(text, font, color, center):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=center)
        screen.blit(surface, rect)

    running = True
    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

            elif state == "playing" and event.type == MOUSEBUTTONDOWN and event.button == 1:
                if alien_visible and alien_rect.collidepoint(event.pos):
                    current_alien_index += 1
                    alien_visible = False
                    alien_delay_timer = current_time + 500  # delay next alien
                    if current_alien_index >= len(levels[level]):
                        # Level completed
                        score += level_points[level]
                        if score >= 60:
                            lives += 2
                            score = 0
                        elif score >= 30:
                            lives += 1
                            score = 0
                        message_timer = current_time
                        state = "level_won"
                else:
                    # Missed click
                    lives -= 1
                    alien_visible = False
                    alien_delay_timer = current_time + 500
                    if lives <= 0:
                        state = "game_over"

            elif state in ["level_won", "game_over", "game_won"]:
                if event.type in [KEYDOWN, MOUSEBUTTONDOWN]:
                    if state == "level_won":
                        level += 1
                        current_alien_index = 0
                        alien_visible = False
                        alien_timer_start = 0
                        alien_delay_timer = current_time + 1000
                        if level >= len(levels):
                            state = "game_won"
                        else:
                            state = "playing"
                    else:
                        running = False

                        # ALIEN LOGIC
                    if state == "playing":
                        if not alien_visible and current_alien_index < len(levels[level]):
                            if alien_delay_timer == 0:
                                alien_delay_timer = current_time + 500  # small delay before showing first alien

                            elif current_time >= alien_delay_timer:
                                current_alien = levels[level][current_alien_index]
                                alien_rect = current_alien.get_rect(center=(screen_width // 2, screen_height // 2))
                                alien_timer_start = current_time
                                alien_visible = True
                                alien_delay_timer = 0

                        elif alien_visible:
                            if current_time - alien_timer_start >= flash_times[level]:
                                # Time's up, missed alien
                                lives -= 1
                                alien_visible = False
                                alien_delay_timer = current_time + 500
                                if lives <= 0:
                                    state = "game_over"

                        # HUD
                    draw_text(f"Lives: {lives}  Score: {score}  Level: {level + 1}/21", font_small, (255, 255, 255),
                              (screen_width // 2, 30))

                    if alien_visible and current_alien:
                        screen.blit(current_alien, alien_rect)

                    # Level messages
                    if state == "level_won":
                        draw_text(f"Level {level + 1} Won!", font_large, (255, 255, 0),
                                  (screen_width // 2, screen_height // 2))

                    elif state == "game_over":
                        draw_text("Game Over", font_large, (255, 0, 0), (screen_width // 2, screen_height // 2))

                    elif state == "game_won":
                        draw_text("You Win!", font_large, (0, 255, 0), (screen_width // 2, screen_height // 2))

                    pygame.display.flip()
                    clock.tick(60)

                pygame.quit()
                sys.exit()

            if __name__ == "__main__":
                main()