import pygame
import sys
import random
import math

pygame.init()

# --- Screen Setup ---
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LEGEND OF WARRIOR")
clock = pygame.time.Clock()

# --- Helper to load and resize images ---
def load_img(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# --- Load Backgrounds ---
bg_home = load_img("images/home_bg.png", (WIDTH, HEIGHT))
bg_levels = [
    load_img("images/bg_level1.png", (WIDTH, HEIGHT)),
    load_img("images/bg_level2.png", (WIDTH, HEIGHT)),
    load_img("images/bg_level3.png", (WIDTH, HEIGHT))
]

# --- Fireball Images ---
fireball_img = load_img("images/fireballstraingt.png", (40, 40))
fireball_fly_img = load_img("images/fireballleftwownord.png", (40, 40))

# --- Warrior Images ---
warrior_imgs = [
    {
        "stand": load_img("images/warrior_lvl1.png", (150, 150)),
        "jump": load_img("images/warrior_jump_lvl1.png", (150, 150)),
        "attack": load_img("images/warrior_attack__lvl1.png", (150, 150))
    },
    {
        "stand": load_img("images/warrior_lvl2.png", (160, 160)),
        "jump": load_img("images/warrior_jump_lvl2.png", (160, 160)),
        "attack": load_img("images/warrior_attack_lvl2.png", (160, 160))
    },
    {
        "stand": load_img("images/warrior_lvl3.png", (170, 170)),
        "jump": load_img("images/warrior_jump_lvl3.png", (170, 170)),
        "attack": load_img("images/warrior_attack_lvl3.png", (170, 170))
    }
]

# --- Monster Images ---
monster_imgs = [
    {
        "stand": load_img("images/monster_lvl1.png", (160, 160)),
        "attack": load_img("images/monster_attack_lvl1.png", (160, 160))
    },
    {
        "stand": load_img("images/monster_lvl2.png", (180, 180)),
        "attack": load_img("images/monster_attack_lvl2.png", (180, 180))
    },
    {
        "stand": load_img("images/monster_lvl3.png", (200, 200)),
        "attack": load_img("images/monster_attack_lvl3.png", (200, 200))
    }
]

# --- Fonts ---
font_title = pygame.font.SysFont("impact", 70)
font_label = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 30, bold=True)

# --- Classes ---

class Warrior:
    def __init__(self, level):
        self.images = warrior_imgs[level - 1]
        self.image = self.images["stand"]
        self.x, self.y = 100, 400
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.attacking = False
        self.attack_timer = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if not self.jumping and keys[pygame.K_UP]:
            self.jumping = True
            self.vel_y = -15

        if self.jumping:
            self.y += self.vel_y
            self.vel_y += 1
            if self.y >= 400:
                self.y = 400
                self.jumping = False

    def attack(self):
        self.attacking = True
        self.attack_timer = pygame.time.get_ticks()

    def draw(self):
        now = pygame.time.get_ticks()
        if self.attacking and now - self.attack_timer < 500:
            self.image = self.images["attack"]
        elif self.jumping:
            self.image = self.images["jump"]
        else:
            self.image = self.images["stand"]
        screen.blit(self.image, (self.x, self.y))


class Monster:
    def __init__(self, level):
        self.images = monster_imgs[level - 1]
        self.image = self.images["stand"]
        self.x = 750
        self.y = 250 if level == 2 else 400
        self.health = 100  # Default health for initialization

        # Added health scaling based on level without changing other code
        if level == 1:
            self.health = 100  # Same as Hero health
        elif level == 2:
            self.health = 200  # Double Hero health
        elif level == 3:
            self.health = 300  # Triple Hero health

        self.level = level
        self.attack_timer = 0
        self.attack_visible = False

        self.invisible = False
        self.invisible_start_time = 0
        self.invisible_duration = 3000

    def attack(self):
        self.attack_visible = True
        self.attack_timer = pygame.time.get_ticks()

    def make_invisible(self):
        self.invisible = True
        self.invisible_start_time = pygame.time.get_ticks()

        angle_to_hero = math.atan2(self.y - game.player.y, self.x - game.player.x)
        offset = random.uniform(-math.pi / 2, math.pi / 2)
        respawn_angle = angle_to_hero + offset
        dist = random.randint(200, 350)
        self.x = int(game.player.x + dist * math.cos(respawn_angle))
        self.y = int(game.player.y + dist * math.sin(respawn_angle))

        if self.level != 2:
            self.y = 400

        self.x = max(0, min(WIDTH - 150, self.x))
        self.y = max(100, min(HEIGHT - 160, self.y))

    def update_invisibility(self):
        if self.invisible:
            now = pygame.time.get_ticks()
            if now - self.invisible_start_time > self.invisible_duration:
                self.invisible = False

    def draw(self):
        self.update_invisibility()
        if self.invisible:
            return
        now = pygame.time.get_ticks()
        if self.attack_visible and now - self.attack_timer < 500:
            self.image = self.images["attack"]
        else:
            self.image = self.images["stand"]
            self.attack_visible = False
        screen.blit(self.image, (self.x, self.y))


class Projectile:
    def __init__(self, x, y, speed_x, speed_y, is_monster=False):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.is_monster = is_monster

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        if self.is_monster:
            screen.blit(fireball_fly_img, (self.x, self.y))
        else:
            screen.blit(fireball_img, (self.x, self.y))


class Game:
    def __init__(self):
        self.state = "home"
        self.level = 1
        self.player = Warrior(self.level)
        self.monster = Monster(self.level)
        self.projectiles = []
        self.monster_projectiles = []

    def reset_level(self):
        self.player = Warrior(self.level)
        self.monster = Monster(self.level)
        self.projectiles.clear()
        self.monster_projectiles.clear()

    def draw_health(self):
        draw_text("PLAYER HEALTH", font_label, (255, 255, 255), 50, 20)
        draw_text("MONSTER HEALTH", font_label, (255, 255, 255), 750, 20)

        pygame.draw.rect(screen, (255, 255, 255), (48, 58, 204, 24))
        pygame.draw.rect(screen, (0, 255, 0), (50, 60, self.player.health * 2, 20))

        pygame.draw.rect(screen, (255, 255, 255), (748, 58, 204, 24))
        pygame.draw.rect(screen, (255, 0, 0), (750, 60, self.monster.health, 20))

    def handle_player_attacks(self, keys):
        if keys[pygame.K_a]:
            self.player.attack()
            if abs(self.player.x - self.monster.x) < 120:
                self.monster.health -= 0.4

        if keys[pygame.K_s]:
            if len(self.projectiles) < 3:
                self.projectiles.append(Projectile(self.player.x + 100, self.player.y + 60, 10, 0))

        if keys[pygame.K_d]:
            if len(self.projectiles) < 2:
                self.projectiles.append(Projectile(self.player.x + 100, self.player.y + 60, 8, 0))

    def monster_attack_logic(self):
        if random.randint(1, 80) == 1:
            self.monster.attack()
            dx = self.player.x - self.monster.x
            dy = (self.player.y - self.monster.y) + 40
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist
            speed = 7
            self.monster_projectiles.append(
                Projectile(self.monster.x, self.monster.y + 60, dx * speed, dy * speed, True)
            )

        if not self.monster.invisible and random.randint(1, 300) == 1:
            self.monster.make_invisible()

        distance = math.hypot(self.monster.x - self.player.x, self.monster.y - self.player.y)
        if distance < 120:
            self.player.health -= 0.5

    def check_collisions(self):
        for p in self.projectiles[:]:
            if self.monster.x < p.x < self.monster.x + 150 and self.monster.y < p.y < self.monster.y + 150:
                self.monster.health -= 2
                self.projectiles.remove(p)
            elif p.x > WIDTH:
                self.projectiles.remove(p)

        for m in self.monster_projectiles[:]:
            if self.player.x < m.x < self.player.x + 150 and self.player.y < m.y < self.player.y + 150:
                self.player.health -= 3
                self.monster_projectiles.remove(m)
            elif m.x < 0 or m.y > HEIGHT or m.y < 0:
                self.monster_projectiles.remove(m)

    def update_play(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.handle_player_attacks(keys)
        self.monster_attack_logic()
        self.check_collisions()

        screen.blit(bg_levels[self.level - 1], (0, 0))
        self.player.draw()
        self.monster.draw()
        self.draw_health()

        text = f"LEVEL {self.level}"
        outline = font_title.render(text, True, (0, 0, 0))
        label = font_title.render(text, True, (255, 255, 0))
        screen.blit(outline, (WIDTH // 2 - 140, 98))
        screen.blit(label, (WIDTH // 2 - 140, 90))

        for p in self.projectiles:
            p.move()
            p.draw()
        for m in self.monster_projectiles:
            m.move()
            m.draw()

        if self.player.health <= 0:
            self.state = "over"
        elif self.monster.health <= 0:
            if self.level < 3:
                self.level += 1
                self.reset_level()
            else:
                self.state = "win"

    def show_home(self):
        screen.blit(bg_home, (0, 0))
        draw_text("LEGEND OF WARRIOR", font_title, (255, 255, 255), 240, 150)

        pygame.draw.rect(screen, (20, 20, 20), (360, 330, 280, 60), border_radius=15)
        pygame.draw.rect(screen, (200, 200, 0), (360, 330, 280, 60), 3, border_radius=15)
        draw_text("Press ENTER to Start", font_small, (255, 255, 0), 370, 340)

        pygame.draw.rect(screen, (50, 50, 50), (360, 410, 280, 60), border_radius=15)
        pygame.draw.rect(screen, (200, 0, 0), (360, 410, 280, 60), 3, border_radius=15)
        draw_text("Press Q to Exit", font_small, (255, 80, 80), 400, 420)

    def show_end(self, win=False):
        screen.fill((0, 0, 0))
        if win:
            draw_text("🏆 YOU WON ALL LEVELS! 🏆", font_title, (255, 215, 0), 200, 250)
        else:
            draw_text("💀 GAME OVER 💀", font_title, (255, 0, 0), 300, 250)
        draw_text("Press ESC to return Home", font_small, (255, 255, 255), 340, 330)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == "home":
                    if event.key == pygame.K_RETURN:
                        self.state = "play"
                        self.level = 1
                        self.reset_level()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "home"
                    self.reset_level()

        if self.state == "home":
            self.show_home()
        elif self.state == "play":
            self.update_play()
        elif self.state == "win":
            self.show_end(win=True)
        elif self.state == "over":
            self.show_end(win=False)


# --- Text Drawing Helper ---
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# --- MAIN LOOP ---
game = Game()
while True:
    game.run()
    pygame.display.update()
    clock.tick(60)
