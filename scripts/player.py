import pygame, os
from animation import load_animations, Animator
from projectiles import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"warrior_lvl{level}.png")

        # adjust frame size/columns/rows to match your sheets
        frame_w, frame_h = 128, 128
        columns, rows = 5, 4
        action_names = ["idle", "run", "attack", "jump"]
        animations = load_animations(sheet, frame_w, frame_h, columns, rows, action_names)

        self.animator = Animator(animations, frame_time=90)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(200, 520))
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.projectiles = []

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if not self.jumping and keys[pygame.K_UP]:
            self.jumping, self.vel_y = True, -15
        if self.jumping:
            self.rect.y += self.vel_y
            self.vel_y += 1
            if self.rect.y >= 400:
                self.rect.y, self.jumping = 400, False

    def attack(self, audio):
        self.animator.set_animation("attack")
        audio.play_sfx("sword")

    def fireball(self, audio):
        if len(self.projectiles) < 3:
            audio.play_sfx("fireball")
            fireball = Projectile(self.rect.centerx + 30, self.rect.centery - 20, 10, 0, is_monster=False)
            self.projectiles.append(fireball)

    def update(self, keys, audio):
        # input-driven actions
        if keys[pygame.K_a] or keys[pygame.K_SPACE]:
            self.attack(audio)
        elif keys[pygame.K_s]:
            self.fireball(audio)
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.animator.set_animation("run")
        elif self.jumping:
            self.animator.set_animation("jump")
        else:
            self.animator.set_animation("idle")

        self.image = self.animator.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
