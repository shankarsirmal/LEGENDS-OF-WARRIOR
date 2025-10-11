import pygame
import sys
import random

pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LEGEND OF WARRIOR")

clock = pygame.time.Clock()

# --- Function to load and resize images ---
def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)

# --- Load backgrounds ---
bg_home = load_image("images/home_bg.png", (WIDTH, HEIGHT))
bg_levels = [
    load_image("images/bg_level1.png", (WIDTH, HEIGHT)),
    load_image("images/bg_level2.png", (WIDTH, HEIGHT)),
    load_image("images/bg_level3.png", (WIDTH, HEIGHT))
]

# --- Load warriors ---
warriors = [
    load_image("images/warrior_lvl1.png", (110, 110)),
    load_image("images/warrior_lvl2.png", (120, 120)),
    load_image("images/warrior_lvl3.png", (130, 130))
]

# --- Load monsters ---
monsters = [
    load_image("images/monster_lvl1.png", (130, 130)),
    load_image("images/monster_lvl2.png", (140, 140)),
    load_image("images/monster_lvl3.png", (160, 160))
]

# --- Game states ---
HOME, PLAY, WIN, GAME_OVER = "home", "play", "win", "over"
state = HOME

level = 1
MAX_LEVEL = 3

# --- Player and monster data ---
player = {"x": 100, "y": 400, "vel_y": 0, "jump": False, "health": 100}
monster = {"x": 750, "y": 400, "attack_timer": 0, "health": 100}

# --- Projectiles ---
arrows, fireballs, monster_attacks = [], [], []

gravity = 1
font = pygame.font.SysFont("Arial", 36)

# --- Helper Functions ---
def draw_text(text, size, color, x, y):
    font_ = pygame.font.SysFont("Arial", size)
    label = font_.render(text, True, color)
    screen.blit(label, (x, y))

def draw_health(x, y, health, color):
    pygame.draw.rect(screen, (255, 255, 255), (x - 2, y - 2, 204, 24))
    pygame.draw.rect(screen, color, (x, y, max(0, health) * 2, 20))

def reset_level():
    player.update({"x": 100, "y": 400, "jump": False, "vel_y": 0, "health": 100})
    monster.update({"x": 750, "y": 400, "attack_timer": 0, "health": 100})
    arrows.clear()
    fireballs.clear()
    monster_attacks.clear()

# --- Home Screen ---
def show_home():
    screen.blit(bg_home, (0, 0))
    draw_text("LEGEND OF WARRIOR", 60, (255, 255, 255), 250, 150)
    draw_text("Press ENTER to Start", 35, (255, 255, 0), 370, 330)
    draw_text("Press Q to Quit", 30, (255, 0, 0), 420, 380)

# --- Play Game Function ---
def play_game():
    global level, state

    idx = level - 1
    screen.blit(bg_levels[idx], (0, 0))

    # Draw characters
    screen.blit(warriors[idx], (player["x"], player["y"]))
    screen.blit(monsters[idx], (monster["x"], monster["y"]))

    # Health bars
    draw_health(50, 50, player["health"], (0, 255, 0))
    draw_health(750, 50, monster["health"], (255, 0, 0))
    draw_text(f"LEVEL {level}", 40, (255, 255, 255), 440, 10)

    keys = pygame.key.get_pressed()

    # Movement
    if keys[pygame.K_LEFT]:
        player["x"] -= 5
    if keys[pygame.K_RIGHT]:
        player["x"] += 5

    # Jump
    if not player["jump"] and keys[pygame.K_UP]:
        player["jump"] = True
        player["vel_y"] = -15

    # Bend
    if keys[pygame.K_DOWN]:
        player["y"] = 450
    elif not player["jump"]:
        player["y"] = 400

    # Gravity
    if player["jump"]:
        player["y"] += player["vel_y"]
        player["vel_y"] += gravity
        if player["y"] >= 400:
            player["y"] = 400
            player["jump"] = False

    # --- Player attacks ---
    if keys[pygame.K_a]:  # Sword
        draw_text("🗡️", 40, (255, 215, 0), player["x"] + 80, player["y"])
        if abs(player["x"] - monster["x"]) < 120:
            monster["health"] -= 0.4

    if keys[pygame.K_s]:  # Arrow
        if len(arrows) < 3:
            arrows.append([player["x"] + 80, player["y"] + 40])

    if keys[pygame.K_d]:  # Fireball
        if len(fireballs) < 2:
            fireballs.append([player["x"] + 80, player["y"] + 40])

    # --- Move Arrows ---
    for arrow in arrows[:]:
        arrow[0] += 10
        pygame.draw.circle(screen, (255, 255, 0), (arrow[0], arrow[1]), 5)
        if arrow[0] > WIDTH:
            arrows.remove(arrow)
        elif monster["x"] < arrow[0] < monster["x"] + 100 and monster["y"] < arrow[1] < monster["y"] + 100:
            monster["health"] -= 1
            arrows.remove(arrow)

    # --- Move Fireballs ---
    for fb in fireballs[:]:
        fb[0] += 8
        pygame.draw.circle(screen, (255, 80, 0), (fb[0], fb[1]), 10)
        if fb[0] > WIDTH:
            fireballs.remove(fb)
        elif monster["x"] < fb[0] < monster["x"] + 100 and monster["y"] < fb[1] < monster["y"] + 100:
            monster["health"] -= 2
            fireballs.remove(fb)

    # --- Monster attacks ---
    monster["attack_timer"] += 1
    if monster["attack_timer"] > 60:
        monster["attack_timer"] = 0
        monster_attacks.append([monster["x"], monster["y"] + 40])

    for atk in monster_attacks[:]:
        atk[0] -= 7
        pygame.draw.circle(screen, (255, 0, 0), (atk[0], atk[1]), 10)
        if atk[0] < 0:
            monster_attacks.remove(atk)
        elif player["x"] < atk[0] < player["x"] + 100 and player["y"] < atk[1] < player["y"] + 100:
            player["health"] -= 2
            monster_attacks.remove(atk)

    # --- Check Game State ---
    if player["health"] <= 0:
        state = GAME_OVER
    elif monster["health"] <= 0:
        if level < MAX_LEVEL:
            level += 1
            reset_level()
        else:
            state = WIN

# --- Win / Game Over Screens ---
def show_win():
    screen.fill((0, 0, 0))
    draw_text("🏆 YOU WON ALL LEVELS! 🏆", 60, (255, 215, 0), 250, 250)
    draw_text("Press ESC to return Home", 30, (255, 255, 255), 360, 320)

def show_game_over():
    screen.fill((0, 0, 0))
    draw_text("💀 GAME OVER 💀", 60, (255, 0, 0), 350, 250)
    draw_text("Press ESC to return Home", 30, (255, 255, 255), 360, 320)

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if state == HOME:
                if event.key == pygame.K_RETURN:
                    state = PLAY
                    level = 1
                    reset_level()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.key == pygame.K_ESCAPE:
                state = HOME
                reset_level()

    # --- Page Display ---
    if state == HOME:
        show_home()
    elif state == PLAY:
        play_game()
    elif state == WIN:
        show_win()
    elif state == GAME_OVER:
        show_game_over()

    pygame.display.update()
    clock.tick(60)
