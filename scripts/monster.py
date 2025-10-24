import pygame, os, random, math
from animation import load_animations, Animator
from projectiles import Projectile

class Monster(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"monster_lvl{level}.png")

        animations = load_animations(sheet, 128, 128, 5, 2, ["idle", "attack"])
        self.animator = Animator(animations, 100)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(800, 520))

        self.health = 100
        self.level = level
        self.projectiles = []

        self.invisible = False
        self.invisible_timer = 0
        self.invisible_duration = 1500

        self.visible_start = pygame.time.get_ticks()
        self.visible_duration = random.randint(5000, 10000)

        self.respawn_radius = 200
        self.proximity_radius = 120
        self.proximity_damage = 0.2

    def become_invisible(self):
        self.invisible = True
        self.invisible_timer = pygame.time.get_ticks()

    def respawn_near_player(self, player):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(60, self.respawn_radius)
        x = int(player.rect.centerx + math.cos(angle) * dist)
        x = max(0, min(x, 1550))
        self.rect.midbottom = (x, 520)
        self.invisible = False
        self.visible_start = pygame.time.get_ticks()
        self.visible_duration = random.randint(5000, 10000)

    def attack(self, player, audio):
        self.animator.set_animation("attack")
        audio.play_sfx(f"monster{min(self.level, 2)}")
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        self.projectiles.append(Projectile(self.rect.centerx, self.rect.centery, dx / dist * 8, dy / dist * 8, True))

    def update(self, player, audio):
        now = pygame.time.get_ticks()
        if self.invisible:
            if now - self.invisible_timer > self.invisible_duration:
                self.respawn_near_player(player)
            return

        if now - self.visible_start > self.visible_duration and random.randint(1, 100) == 1:
            self.become_invisible()
            return

        dist = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        if dist < self.proximity_radius:
            player.health = max(0, player.health - self.proximity_damage)

        if random.randint(1, 100) == 1:
            self.attack(player, audio)

        self.image = self.animator.update()

    def draw(self, screen):
        if not self.invisible:
            screen.blit(self.image, self.rect)
