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


import pygame
import random
import sys

pygame.init()

screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alien Capture")

clock = pygame.time.Clock()
FPS = 60

# Load background
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

confetti_img = pygame.image.load("assets/confetti.png")
confetti_img = pygame.transform.scale(confetti_img, (900, 600))

# Load all 29 aliens
alien_images = []
for i in range(1, 30):
    try:
        img = pygame.image.load(f"assets/alien{i}.png")
        img = pygame.transform.scale(img, (260, 400))
        alien_images.append(img)
    except:
        print(f"Could not load alien{i}.png")

# Fonts
font = pygame.font.Font(f"assets/lands.otf", 36)
bday_font = pygame.font.Font(f"assets/bday.otf", 70)
gameover_font = pygame.font.Font(f"assets/gameover.otf", 30)
replay_font = pygame.font.Font(None, 32)

# Replay button
replay_button = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 70, 160, 45)

def draw_text(text, colour, x, y, font_used=font):
    label = font_used.render(text, True, colour)
    screen.blit(label, (x, y))

# Game state
def reset_game():
    global lives, score, game_over, alien_visible, last_flash
    lives = 3
    score = 0
    game_over = False
    alien_visible = False
    last_flash = pygame.time.get_ticks()

reset_game()

# Alien flashing logic
alien_flash_time = 500
current_alien = random.choice(alien_images)
alien_rect = current_alien.get_rect()
show_message = False
message_timer = 0

run = True
while run:
    screen.blit(background, (0, 0))
    current_time = pygame.time.get_ticks()

    if not game_over:
        if not alien_visible and current_time - last_flash >= random.randint(1000, 3000):
            current_alien = random.choice(alien_images)
            rand_x = random.randint(100, screen_width - 260)
            rand_y = random.randint(100, screen_height - 400)
            alien_rect = current_alien.get_rect(topleft=(rand_x, rand_y))
            alien_visible = True
            last_flash = current_time

        elif alien_visible and current_time - last_flash >= alien_flash_time:
            alien_visible = False
            last_flash = current_time

    if alien_visible:
        screen.blit(current_alien, alien_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if alien_visible and alien_rect.collidepoint(event.pos):
                    score += 1
                    alien_visible = False
                    last_flash = pygame.time.get_ticks()
                    show_message = True
                    message_timer = current_time
                else:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
            else:
                if replay_button.collidepoint(event.pos):
                    reset_game()

    draw_text(f"Lives: {lives}", (57, 255, 20), 10, 10)
    draw_text(f"Score: {score}", (57, 255, 20), 10, 50)

    if show_message and current_time - message_timer < 2500:
        bday_text = bday_font.render("Happy Birthday!", True, (0, 128, 255))
        bday_rect = bday_text.get_rect(center=(screen_width // 2 - 110, screen_height // 2 - 20))
        screen.blit(bday_text, bday_rect)
        screen.blit(confetti_img, (0, 0))

    else:
        show_message = False

    if game_over:
        gameover_text = gameover_font.render("Game Over", True, (255, 0, 0))
        gameover_rect = gameover_text.get_rect(center=(screen_width // 2 - 100, screen_height // 2))
        screen.blit(gameover_text, gameover_rect)
        # Hover effect
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = replay_button.collidepoint(mouse_pos)


        button_color = (30, 144, 255) if not is_hovered else (0, 191, 255)

        # Draw rounded button
        pygame.draw.rect(screen, button_color, replay_button, border_radius=25)

        # Draw Replay text centered inside button
        replay_text = replay_font.render("Replay", True, (255, 255, 255))
        text_rect = replay_text.get_rect(center=replay_button.center)
        screen.blit(replay_text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

import pygame
import random
import sys

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Load and play background music
try:
    pygame.mixer.music.load("assets/music2.mp3")  # Or .ogg
    pygame.mixer.music.play(-1)  # -1 means it loops forever
    pygame.mixer.music.set_volume(0.5)  # Optional: Volume from 0.0 to 1.0
except:
    print("Could not load or play music.")


screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alien Capture")

clock = pygame.time.Clock()
FPS = 60

# Load background
try:
    background = pygame.image.load("assets/background.PNG")
    background = pygame.transform.scale(background, (screen_width, screen_height))
except:
    print("Error: Could not load background image.")
    pygame.quit()
    sys.exit()

# Load confetti image
try:
    confetti_img = pygame.image.load("assets/confetti.png")
    confetti_img = pygame.transform.scale(confetti_img, (900, 600))
except:
    print("Error: Could not load confetti image.")
    confetti_img = None

# Load all 29 aliens
alien_images = []
for i in range(1, 30):
    try:
        img = pygame.image.load(f"assets/alien{i}.png")
        img = pygame.transform.scale(img, (260, 400))
        alien_images.append(img)
    except:
        print(f"Warning: Could not load alien{i}.png")

if not alien_images:
    print("No alien images loaded. Exiting.")
    pygame.quit()
    sys.exit()

# Fonts
try:
    font = pygame.font.Font("assets/lands.otf", 36)
except:
    font = pygame.font.SysFont("arial", 36)

try:
    bday_font = pygame.font.Font("assets/bday.ttf", 50)
except:
    bday_font = pygame.font.SysFont("arial", 70)

try:
    gameover_font = pygame.font.Font("assets/gameover.otf", 30)
except:
    gameover_font = pygame.font.SysFont("arial", 30)

replay_font = pygame.font.Font("assets/replay.ttf", 24)

# Replay button
replay_button = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 70, 160, 45)

def draw_text(text, colour, x, y, font_used=font):
    label = font_used.render(text, True, colour)
    screen.blit(label, (x, y))

# Game state
def reset_game():
    global lives, score, game_over, alien_visible, last_flash
    lives = 3
    score = 0
    game_over = False
    alien_visible = False
    last_flash = pygame.time.get_ticks()

reset_game()

# Alien flashing logic
alien_flash_time = 500
current_alien = random.choice(alien_images)
alien_rect = current_alien.get_rect()
show_message = False
message_timer = 0

run = True
while run:
    screen.blit(background, (0, 0))
    current_time = pygame.time.get_ticks()

    if not game_over:
        if not alien_visible and current_time - last_flash >= random.randint(1000, 3000):
            current_alien = random.choice(alien_images)
            rand_x = random.randint(100, screen_width - 260)
            rand_y = random.randint(100, screen_height - 400)
            alien_rect = current_alien.get_rect(topleft=(rand_x, rand_y))
            alien_visible = True
            last_flash = current_time

        elif alien_visible and current_time - last_flash >= alien_flash_time:
            alien_visible = False
            last_flash = current_time

    if alien_visible:
        screen.blit(current_alien, alien_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if alien_visible and alien_rect.collidepoint(event.pos):
                    score += 1
                    alien_visible = False
                    last_flash = pygame.time.get_ticks()
                    show_message = True
                    message_timer = current_time
                else:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
            else:
                if replay_button.collidepoint(event.pos):
                    reset_game()

    draw_text(f"Lives: {lives}", (57, 255, 20), 10, 10)
    draw_text(f"Score: {score}", (57, 255, 20), 10, 50)

    if show_message and current_time - message_timer < 1000:
        bday_text = bday_font.render("Happy Birthday!", True, (65, 105, 225))
        bday_rect = bday_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(bday_text, bday_rect)
        if confetti_img:
            screen.blit(confetti_img, (0, 0))
    else:
        show_message = False

    if game_over:
        gameover_text = gameover_font.render("Game Over", True, (255, 0, 0))
        gameover_rect = gameover_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(gameover_text, gameover_rect)

        mouse_pos = pygame.mouse.get_pos()
        is_hovered = replay_button.collidepoint(mouse_pos)
        button_color = (57, 255, 20) if not is_hovered else (0, 191, 255)

        pygame.draw.rect(screen, button_color, replay_button, border_radius=25)
        replay_text = replay_font.render("Replay", True, (0, 0, 0))
        text_rect = replay_text.get_rect(center=replay_button.center)
        screen.blit(replay_text, text_rect)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()


import pygame
import random
import sys

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Load and play background music
try:
    pygame.mixer.music.load("assets/music2.mp3")  # Or .ogg
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
except:
    print("Could not load or play music.")

screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Alien Capture")

clock = pygame.time.Clock()
FPS = 60

# Load background
try:
    background = pygame.image.load("assets/background.PNG")
    background = pygame.transform.scale(background, (screen_width, screen_height))
except:
    print("Error: Could not load background image.")
    pygame.quit()
    sys.exit()

# Load confetti image
try:
    confetti_img = pygame.image.load("assets/confetti.png")
    confetti_img = pygame.transform.scale(confetti_img, (900, 600))
except:
    confetti_img = None

# Load older Ben 10 image
try:
    ben10_adult = pygame.image.load("assets/ben10_adult.png")
    ben10_adult = pygame.transform.scale(ben10_adult, (300, 400))
except:
    ben10_adult = None

# Load all 29 aliens
alien_images = []
for i in range(1, 30):
    try:
        img = pygame.image.load(f"assets/alien{i}.png")
        img = pygame.transform.scale(img, (260, 400))
        alien_images.append(img)
    except:
        print(f"Warning: Could not load alien{i}.png")

if not alien_images:
    print("No alien images loaded. Exiting.")
    pygame.quit()
    sys.exit()

# Fonts
try:
    font = pygame.font.Font("assets/lands.otf", 36)
except:
    font = pygame.font.SysFont("arial", 36)

try:
    bday_font = pygame.font.Font("assets/bday.ttf", 50)
except:
    bday_font = pygame.font.SysFont("arial", 70)

try:
    gameover_font = pygame.font.Font("assets/gameover.otf", 30)
except:
    gameover_font = pygame.font.SysFont("arial", 30)

replay_font = pygame.font.Font("assets/replay.ttf", 24)

# Replay button
replay_button = pygame.Rect(screen_width // 2 - 80, screen_height // 2 + 70, 160, 45)

# Helper function to draw text
def draw_text(text, colour, x, y, font_used=font):
    label = font_used.render(text, True, colour)
    screen.blit(label, (x, y))

# Welcome message
def show_start_screen():
    screen.fill((0, 0, 0))
    surprise_text = font.render("Score 21 for a surprise!", True, (57, 255, 20))
    surprise_rect = surprise_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    screen.blit(surprise_text, surprise_rect)

    start_text = font.render("Click to Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    screen.blit(start_text, start_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

show_start_screen()

# Game state
def reset_game():
    global lives, score, game_over, alien_visible, last_flash, special_shown
    lives = 3
    score = 0
    game_over = False
    alien_visible = False
    special_shown = False
    last_flash = pygame.time.get_ticks()

reset_game()

# Alien flashing logic
alien_flash_time = 500
current_alien = random.choice(alien_images)
alien_rect = current_alien.get_rect()
show_message = False
message_timer = 0

run = True
while run:
    screen.blit(background, (0, 0))
    current_time = pygame.time.get_ticks()

    if not game_over:
        if not alien_visible and current_time - last_flash >= random.randint(1000, 3000):
            current_alien = random.choice(alien_images)
            rand_x = random.randint(100, screen_width - 260)
            rand_y = random.randint(100, screen_height - 400)
            alien_rect = current_alien.get_rect(topleft=(rand_x, rand_y))
            alien_visible = True
            last_flash = current_time

        elif alien_visible and current_time - last_flash >= alien_flash_time:
            alien_visible = False
            last_flash = current_time

    if alien_visible:
        screen.blit(current_alien, alien_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if alien_visible and alien_rect.collidepoint(event.pos):
                    score += 1
                    alien_visible = False
                    last_flash = pygame.time.get_ticks()
                    show_message = True
                    message_timer = current_time
                else:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
            else:
                if replay_button.collidepoint(event.pos):
                    reset_game()

    # Draw UI
    draw_text(f"Lives: {lives}", (57, 255, 20), 10, 10)
    draw_text(f"Score: {score}", (57, 255, 20), 10, 50)

    # Birthday message
    if show_message and current_time - message_timer < 1000:
        bday_text = bday_font.render("Happy Birthday!", True, (65, 105, 225))
        bday_rect = bday_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(bday_text, bday_rect)
        if confetti_img:
            screen.blit(confetti_img, (0, 0))
    else:
        show_message = False

    # Surprise message when score hits 21
    if score >= 2 and not special_shown:
        screen.fill((0, 0, 0))
        if ben10_adult:
            screen.blit(ben10_adult, ((screen_width - ben10_adult.get_width()) // 2, 50))
        message_text = bday_font.render("Little Varun, you're a strong and coolest grown-up now!", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(screen_width // 2, screen_height - 100))
        screen.blit(message_text, message_rect)
        pygame.display.flip()
        pygame.time.wait(4000)
        special_shown = True

    if game_over:
        gameover_text = gameover_font.render("Game Over", True, (255, 0, 0))
        gameover_rect = gameover_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(gameover_text, gameover_rect)

        mouse_pos = pygame.mouse.get_pos()
        is_hovered = replay_button.collidepoint(mouse_pos)
        button_color = (57, 255, 20) if not is_hovered else (0, 191, 255)

        pygame.draw.rect(screen, button_color, replay_button, border_radius=25)
        replay_text = replay_font.render("Replay", True, (0, 0, 0))
        text_rect = replay_text.get_rect(center=replay_button.center)
        screen.blit(replay_text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

if score >= 21 and not special_shown:
    game_over = True
    special_shown = True
    screen.fill((0, 0, 0))
    if ben10_adult:
        screen.blit(ben10_adult, (0, 0))
    if confetti_img:
        screen.blit(confetti_img, (0, 0))
    message_text = bday_font.render("Little Varun, you're a strong and coolest grown-up now!", True, (57, 255, 20))
    message_rect = message_text.get_rect(center=(screen_width // 2, screen_height - 60))
    screen.blit(message_text, message_rect)
