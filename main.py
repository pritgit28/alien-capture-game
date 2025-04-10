import pygame
import random
import asyncio
import sys
import os

# Handle asset paths whether running from source or bundled .exe
base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

def asset_path(relative_path):
    return os.path.join(base_path, relative_path)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Screen setup
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Alien Capture")
clock = pygame.time.Clock()
FPS = 60

# Game state
lives = 3
score = 0
game_over = False
alien_visible = False
special_shown = False
last_flash = 0
alien_flash_time = 500
show_message = False
message_timer = 0

# Load assets
try:
    pygame.mixer.music.load(asset_path("assets/music2.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
except:
    print("Could not load or play music.")

try:
    background = pygame.image.load(asset_path("assets/background.PNG"))
    background = pygame.transform.scale(background, (screen_width, screen_height))
except:
    print("Error: Could not load background image.")
    pygame.quit()
    sys.exit()

try:
    confetti_img = pygame.image.load(asset_path("assets/confetti.png"))
    confetti_img = pygame.transform.scale(confetti_img, (900, 600))
except:
    confetti_img = None

try:
    ben10_adult = pygame.image.load(asset_path("assets/ben10_adult.png"))
    ben10_adult = pygame.transform.scale(ben10_adult, (screen_width, screen_height))
except:
    ben10_adult = None

alien_images = []
for i in range(1, 30):
    try:
        img = pygame.image.load(asset_path(f"assets/alien{i}.png"))
        img = pygame.transform.scale(img, (260, 400))
        alien_images.append(img)
    except:
        print(f"Warning: Could not load alien{i}.png")

if not alien_images:
    print("No alien images loaded. Exiting.")
    pygame.quit()
    sys.exit()

try:
    font = pygame.font.Font(asset_path("assets/lands.otf"), 36)
except:
    font = pygame.font.SysFont("arial", 36)

try:
    bday_font = pygame.font.Font(asset_path("assets/bday.ttf"), 28)
except:
    bday_font = pygame.font.SysFont("arial", 28)

try:
    gameover_font = pygame.font.Font(asset_path("assets/gameover.otf"), 30)
except:
    gameover_font = pygame.font.SysFont("arial", 30)

replay_font = pygame.font.Font(asset_path("assets/replay.ttf"), 18)
replay_button = pygame.Rect(screen_width - 140, 20, 120, 40)
current_alien = random.choice(alien_images)
alien_rect = current_alien.get_rect()

# Text drawing
def draw_text(text, colour, x, y, font_used=font):
    label = font_used.render(text, True, colour)
    screen.blit(label, (x, y))

# Start screen
def show_start_screen():
    screen.fill((0, 0, 0))
    surprise_text = font.render("Score 21 for a surprise!", True, (57, 255, 20))
    start_text = font.render("Click to Start", True, (255, 255, 255))
    screen.blit(surprise_text, surprise_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40)))
    screen.blit(start_text, start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20)))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Reset
def reset_game():
    global lives, score, game_over, alien_visible, last_flash, special_shown
    lives = 3
    score = 0
    game_over = False
    alien_visible = False
    special_shown = False
    last_flash = pygame.time.get_ticks()
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(asset_path("assets/music2.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except:
        print("Could not reload music.")

# Main game loop
async def main():
    global lives, score, game_over, alien_visible, special_shown, last_flash
    global current_alien, alien_rect, show_message, message_timer

    show_start_screen()
    reset_game()
    run = True

    while run:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()

        if not game_over and not special_shown:
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
                if not game_over and not special_shown:
                    if alien_visible and alien_rect.collidepoint(event.pos):
                        score += 1
                        alien_visible = False
                        last_flash = pygame.time.get_ticks()
                        show_message = True
                        message_timer = current_time
                    else:
                        lives -= 1
                elif (game_over or special_shown) and replay_button.collidepoint(event.pos):
                    reset_game()

        if not special_shown:
            draw_text(f"Lives: {lives}", (57, 255, 20), 10, 10)
            draw_text(f"Score: {score}", (57, 255, 20), 10, 50)

        if show_message and current_time - message_timer < 1000:
            bday_text = bday_font.render("Happy Birthday!", True, (30, 144, 255))
            screen.blit(bday_text, bday_text.get_rect(center=(screen_width // 2, screen_height // 2)))
            if confetti_img:
                screen.blit(confetti_img, (0, 0))
        else:
            show_message = False

        if score >= 21 and not special_shown:
            pygame.mixer.music.stop()
            try:
                pygame.mixer.music.load(asset_path("assets/hbd_song.mp3"))
                pygame.mixer.music.play()
            except:
                print("Could not load or play birthday song.")
            game_over = True
            special_shown = True

        if special_shown:
            screen.fill((0, 0, 0))
            if confetti_img:
                screen.blit(confetti_img, (0, 0))
            if ben10_adult:
                screen.blit(ben10_adult, (0, 0))
            lines = [
                "Hey little Varun, you've grown into the strongest",
                "and coolest grown-up now! Happy 21st birthday!"
            ]
            for i, line in enumerate(lines):
                message_text = bday_font.render(line, True, (240, 255, 40))
                screen.blit(message_text, message_text.get_rect(center=(screen_width // 2, screen_height - 100 + i * 40)))
            pygame.draw.rect(screen, (57, 255, 20), replay_button, border_radius=25)
            replay_text = replay_font.render("Replay", True, (0, 0, 0))
            screen.blit(replay_text, replay_text.get_rect(center=replay_button.center))

        if lives <= 0 and not special_shown:
            game_over = True

        if game_over and not special_shown:
            gameover_text = gameover_font.render("Game Over", True, (255, 0, 0))
            screen.blit(gameover_text, gameover_text.get_rect(center=(screen_width // 2, screen_height // 2)))
            mouse_pos = pygame.mouse.get_pos()
            button_color = (0, 191, 255) if replay_button.collidepoint(mouse_pos) else (57, 255, 20)
            pygame.draw.rect(screen, button_color, replay_button, border_radius=25)
            replay_text = replay_font.render("Replay", True, (0, 0, 0))
            screen.blit(replay_text, replay_text.get_rect(center=replay_button.center))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
