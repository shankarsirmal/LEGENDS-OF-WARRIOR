import pygame, sys, os
from player import Player
from monster import Monster
from audio import AudioManager
from ui import draw_text
from game_state import GameState

pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LEGEND OF WARRIOR")
clock = pygame.time.Clock()

def load_image(path, size):
    full_path = os.path.join(os.path.dirname(__file__), "..", "assets", path)
    img = pygame.image.load(full_path).convert_alpha()
    return pygame.transform.scale(img, size)

bg_home = load_image("backgrounds/home_bg.png", (WIDTH, HEIGHT))
bg_levels = [
    load_image("backgrounds/bg_level1.png", (WIDTH, HEIGHT)),
    load_image("backgrounds/bg_level2.png", (WIDTH, HEIGHT)),
    load_image("backgrounds/bg_level3.png", (WIDTH, HEIGHT)),
]

font_title = pygame.font.SysFont("impact", 70)
font_label = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 30, bold=True)

game = GameState(Player, Monster, AudioManager, screen, bg_levels, bg_home)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.handle_event(event)

    game.update(font_label, font_title, font_small)
    pygame.display.update()
    clock.tick(60)
