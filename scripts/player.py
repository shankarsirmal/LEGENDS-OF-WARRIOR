import pygame, os
from animation import load_animations, Animator
from projectiles import Projectile
from config import SPRITE_LAYOUTS

class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"warrior_lvl{level}.png")
        layout = SPRITE_LAYOUTS["warrior"][level]

        animations = load_animations(sheet, layout["columns"], layout["rows"],
                                     layout["actions"], layout["frames_per_row"])

        self.animator = Animator(animations, 100, scale=1.6)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(200, 540))
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.projectiles = []
        self.ground_y = 540  # fixed floor level

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if not self.jumping and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.jumping = True
            self.vel_y = -15
        if self.jumping:
            self.rect.y += self.vel_y
            self.vel_y += 1
            if self.rect.bottom >= self.ground_y:
                self.rect.bottom = self.ground_y
                self.jumping = False
                self.vel_y = 0
        self.rect.clamp_ip(pygame.Rect(0, 0, 1000, 600))

    def attack(self, audio):
        self.animator.set_animation("attack")
        audio.play_sfx("sword")

    def fireball(self, audio):
        if len(self.projectiles) < 3:
            audio.play_sfx("fireball")
            fireball = Projectile(self.rect.centerx + 30, self.rect.centery - 20, 10, 0)
            self.projectiles.append(fireball)

    def update(self, keys, audio):
        if keys[pygame.K_a] or keys[pygame.K_SPACE]:
            self.attack(audio)
        elif keys[pygame.K_s]:
            self.fireball(audio)
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.animator.set_animation("run")
        elif self.jumping:
            self.animator.set_animation("run")
        else:
            self.animator.set_animation("idle")

        self.image = self.animator.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
