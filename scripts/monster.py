import pygame, os, random, math
from animation import load_animations, Animator
from projectiles import Projectile

class Monster(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"monster_lvl{level}.png")

        frame_w, frame_h = 128, 128
        columns, rows = 5, 2
        action_names = ["idle", "attack"]
        animations = load_animations(sheet, frame_w, frame_h, columns, rows, action_names)

        self.animator = Animator(animations, frame_time=100)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(800, 520))
        self.health = 100
        self.level = level
        self.projectiles = []
        self.attack_timer = 0

    def attack(self, player, audio):
        self.animator.set_animation("attack")
        audio.play_sfx(f"monster{min(self.level, 2)}")
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy) or 1
        nx, ny = dx / dist, dy / dist
        self.projectiles.append(Projectile(self.rect.centerx, self.rect.centery, nx * 8, ny * 8, is_monster=True))

    def update(self, player, audio):
        # random attack chance
        if random.randint(1, 100) == 1:
            self.attack(player, audio)
        # animator keeps animating current anim
        self.image = self.animator.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
