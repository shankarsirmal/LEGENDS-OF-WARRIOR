import pygame, os
from animation import load_animations, Animator
from projectiles import Projectile
from config import SPRITE_LAYOUTS

class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        sprites_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")
        sheet = os.path.join(sprites_dir, f"warrior_lvl{level}.png")

        columns, rows = SPRITE_LAYOUTS["warrior"][level]
        sheet_img = pygame.image.load(sheet).convert_alpha()
        frame_w = sheet_img.get_width() // columns
        frame_h = sheet_img.get_height() // rows

        base_actions = ["idle", "run", "attack", "jump", "special"]
        if len(base_actions) < rows:
            base_actions += [f"row{i}" for i in range(len(base_actions), rows)]
        action_names = base_actions[:rows]

        animations = load_animations(sheet, frame_w, frame_h, columns, rows, action_names)
        self.animator = Animator(animations, frame_time=90)

        self.image = self.animator.update()
        self.rect = self.image.get_rect(midbottom=(200, 520))  # aligned baseline
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.projectiles = []
        self.level = level

        # consistent baseline (feet of both player & monster)
        self.ground_bottom = 520

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Jumping
        if not self.jumping and keys[pygame.K_UP]:
            self.jumping = True
            self.vel_y = -18  # stronger jump

        if self.jumping:
            self.rect.y += self.vel_y
            self.vel_y += 1  # gravity
            # stop at baseline
            if self.rect.bottom >= self.ground_bottom:
                self.rect.bottom = self.ground_bottom
                self.jumping = False
                self.vel_y = 0

        # Clamp within screen
        self.rect.x = max(0, min(self.rect.x, 1000 - self.rect.width))

    def attack(self, audio):
        self.animator.set_animation("attack")
        audio.play_sfx("sword")

    def fireball(self, audio):
        if len(self.projectiles) < 3:
            audio.play_sfx("fireball")
            fireball = Projectile(self.rect.centerx + 30, self.rect.centery - 20, 10, 0, False)
            self.projectiles.append(fireball)

    def update(self, keys, audio):
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
