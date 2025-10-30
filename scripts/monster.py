import pygame, os, random, math
from animation import load_animations, Animator
from projectiles import Projectile
from config import SPRITE_LAYOUTS

class Monster(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"monster_lvl{level}.png")

        columns, rows = SPRITE_LAYOUTS["monster"][level]
        sheet_img = pygame.image.load(sheet).convert_alpha()
        frame_w = sheet_img.get_width() // columns
        frame_h = sheet_img.get_height() // rows
        action_names = ["idle", "attack", "walk", "death"][:rows]

        animations = load_animations(sheet, frame_w, frame_h, columns, rows, action_names)
        self.animator = Animator(animations, 100)

        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(800, 520))
        self.health = 100
        self.level = level
        self.projectiles = []
        self.fixed_x = 800

    def attack(self, player, audio):
        self.animator.set_animation("attack")
        audio.play_sfx(f"monster{min(self.level, 3)}")
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        self.projectiles.append(Projectile(self.rect.centerx, self.rect.centery, dx / dist * 8, dy / dist * 8, True))

    def update(self, player, audio):
        self.rect.x = self.fixed_x
        if random.randint(1, 80) == 1:
            self.attack(player, audio)
        dist = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        if dist < 120:
            player.health = max(0, player.health - 0.2)
        self.image = self.animator.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
